from app.models.todo import Todo

_todos: list[Todo] = [
    Todo(id=1, title="Belajar FastAPI", completed=False),
    Todo(id=2, title="Buat endpoint GET todos", completed=True),
    Todo(id=3, title="Tambah POST todo", completed=False),
]


def get_all() -> list[Todo]:
    return list(_todos)


def get_by_id(todo_id: int) -> Todo | None:
    for todo in _todos:
        if todo.id == todo_id:
            return todo
    return None
