from fastapi import FastAPI

from app.routers import todos

app = FastAPI(title="Todo API")

app.include_router(todos.router, prefix="/todos", tags=["todos"])
