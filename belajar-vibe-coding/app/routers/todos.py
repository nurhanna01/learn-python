from fastapi import APIRouter, HTTPException

from app.models.todo import Todo
from app.store import todos as todo_store

router = APIRouter()


@router.get("/", response_model=list[Todo])
def list_todos() -> list[Todo]:
    return todo_store.get_all()


@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: int) -> Todo:
    todo = todo_store.get_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    return todo
