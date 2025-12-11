import uuid
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

from app.engine.graph import Graph
from app.engine.runner import Runner
from app.workflows.code_review import build_sample_graph

router = APIRouter()

GRAPHS: Dict[str, Graph] = {}
RUNNER = Runner()

class GraphRunIn(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]

class GraphRunOut(BaseModel):
    run_id: str
    message: str

@router.post('/graph/create')
async def create_graph():
    graph = build_sample_graph()
    graph_id = str(uuid.uuid4())
    GRAPHS[graph_id] = graph
    return {"graph_id": graph_id}

@router.post('/graph/run', response_model=GraphRunOut)
async def run_graph(payload: GraphRunIn, background_tasks: BackgroundTasks):
    if payload.graph_id not in GRAPHS:
        raise HTTPException(status_code=404, detail='Graph not found')
    graph = GRAPHS[payload.graph_id]
    run_id = RUNNER.create_run(graph, payload.initial_state)
    background_tasks.add_task(RUNNER.execute_run, run_id)
    return {"run_id": run_id, "message": "Run started"}

@router.get('/graph/state/{run_id}')
async def get_state(run_id: str):
    info = RUNNER.get_run_info(run_id)
    if not info:
        raise HTTPException(status_code=404, detail='Run not found')
    return info
