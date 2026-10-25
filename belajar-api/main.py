from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# in memory data
todos = []

# Pydantic model = validasi + skema data (mirip Zod/Joi)
class TodoIn(BaseModel):
    title: str
    done: bool = False

@app.get("/todos")
def list_todos():
    return todos

@app.post("/todos", status_code=201)
def create_todo(body: TodoIn):
    todo = {"id": len(todos) + 1, **body.model_dump()}
    todos.append(todo)
    return todo

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for t in todos:
        if t["id"] == todo_id:
            return t
    raise HTTPException(status_code=404, detail="Todo tidak ditemukan")