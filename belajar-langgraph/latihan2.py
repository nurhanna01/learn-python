from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    angka: int
    percobaan: int

def tambah(state: State) -> dict:
    baru = state["angka"] + 3
    percobaan = state["percobaan"] + 1
    print(f"percobaan ke-{percobaan}: angka jadi {baru}")
    return {"angka": baru, "percobaan": percobaan}

def putuskan(state: State) -> str:
    if state["angka"] >= 10:
        return "selesai"
    if state["percobaan"] >= 5:
        return "menyerah"
    return "ulangi"

graph = StateGraph(State)
graph.add_node("tambah", tambah)
graph.add_edge(START, "tambah")
graph.add_conditional_edges(
    "tambah",
    putuskan,
    {"ulangi": "tambah", "selesai": END, "menyerah": END},
)
app = graph.compile()

print(app.invoke({"angka": 1, "percobaan": 0}))