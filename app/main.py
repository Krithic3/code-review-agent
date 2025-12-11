from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Code Review Mini-Agent")
app.include_router(router)

@app.get("/")
async def root():
    return {"status": "ok", "service": "Code Review Mini-Agent"}
