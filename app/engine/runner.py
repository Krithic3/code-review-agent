import uuid
import asyncio
from typing import Dict, Any, Optional
from app.engine.graph import Graph
from app.engine.registry import ToolRegistry

RUNS: Dict[str, Dict[str, Any]] = {}

class Runner:
    def __init__(self):
        self.runs = RUNS

    def create_run(self, graph: Graph, initial_state: Dict[str, Any]) -> str:
        run_id = str(uuid.uuid4())
        self.runs[run_id] = {
            "graph": graph,
            "state": initial_state.copy(),
            "log": [],
            "status": "created",
        }
        return run_id

    def get_run_info(self, run_id: str) -> Optional[Dict[str, Any]]:
        return self.runs.get(run_id)

    async def _execute_node(self, node_name: str, node, state: Dict[str, Any]):
        func = ToolRegistry.get(node.func_name)
        if asyncio.iscoroutinefunction(func):
            result = await func(state, **node.params)
        else:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, func, state, **node.params)
        return result

    async def _run_graph_async(self, run_id: str):
        run = self.runs[run_id]
        graph: Graph = run["graph"]
        state = run["state"]
        run["status"] = "running"
        current = graph.start

        steps = 0
        max_steps = 1000

        while current:
            if steps >= max_steps:
                run["log"].append("Max steps exceeded, aborting")
                run["status"] = "failed"
                break

            node = graph.nodes[current]
            run["log"].append(f"START {current}")

            try:
                result = await self._execute_node(current, node, state)
            except Exception as e:
                run["log"].append(f"ERROR {current}: {e}")
                run["status"] = "failed"
                break

            if isinstance(result, Dict):
                state.update(result)

            run["log"].append(f"END {current}")

            next_node = None  

            if graph.loops and current in graph.loops:
                cond = graph.loops[current]
                key = cond.get("until")
                threshold = cond.get("threshold")
                val = state.get(key, 0)

                if val < threshold:
                    next_node = cond.get("goto", current)
                    run["log"].append(f"LOOP: {current} → {next_node}")
                else:
                    next_node = graph.edges.get(current)
            else:
                next_node = graph.edges.get(current)

            current = next_node
            steps += 1
            await asyncio.sleep(0)

        if run["status"] != "failed":
            run["status"] = "completed"

        run["state"] = state

    def execute_run(self, run_id: str):
        asyncio.run(self._run_graph_async(run_id))
