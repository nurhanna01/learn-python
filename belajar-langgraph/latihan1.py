from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    angka: int

def tambah(state: State) -> dict:
    return {"angka": state["angka"] + 5}

graph = StateGraph(State)
graph.add_node("tambah", tambah)
graph.add_edge(START, "tambah")
graph.add_edge("tambah", END)

app = graph.compile()
print(app.invoke({"angka": 1}))

