import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from models import TestCaseList
from typing import TypedDict
from langgraph.graph import StateGraph, END, START
from logger import logger_setup, LLMLogger
import logging
from langchain_core.callbacks import BaseCallbackHandler

logger_setup()
log = logging.getLogger(__name__)

load_dotenv()

STANDARDS = {
        "111": "Setiap test case wajib punya skenario negatif. Langkah minimal 3. Langkah maksimal 8.",
        "222": "Prioritas high hanya untuk alur pembayaran.",
}

MAX_PERCOBAAN = 3

class State(TypedDict):
    project_id : str
    feature_description : str
    hasil : TestCaseList
    masalah : str
    percobaan : int

def get_test_rule(project_id: str) -> str:
    """Ambil standar penulisan test case untuk sebuah project.
    Panggil ini sebelum membuat test case supaya formatnya sesuai standar."""
    log.info(f"[TOOL DIPANGGIL] project_id={project_id}")
    if project_id not in STANDARDS:
        log.error(f"Project '{project_id}' tidak dikenal")
        raise ValueError(f"Project '{project_id}' tidak dikenal")
    return STANDARDS.get(project_id, "Standar tidak ditemukan untuk project ini")

_model = ChatOpenAI(
    model="mercury-3",
    api_key=os.environ["INCEPTION_API_KEY"],
    base_url="https://api.inceptionlabs.ai/v1",
    temperature=0.75,
)

_agent = create_agent(
    model=_model,
    tools=[get_test_rule],
    response_format=TestCaseList,
    system_prompt="Kamu QA engineer. Ambil aturan project dulu, lalu buat test case.",
)

def generate(state: State) -> dict :
    try:
        log.debug("============== PEMANGGILAN GENERATE ====================")
        deskripsi = state["feature_description"]
        if state.get("masalah"):
            deskripsi += (
                "\nPerbaiki masalah berikut dari percobaan sebelumnya: \n"
                + "".join(state["masalah"])
            )
        log.debug("==PROMPT KE AI]==>>>>>>", deskripsi)
        
        result = generate_test_cases(state["project_id"],deskripsi)
        percobaan = state.get("percobaan", 0) + 1
        log.debug(f"generate percobaan ke {percobaan},")

        return {"hasil":result, "percobaan":percobaan}
    except Exception as e:
            log.error(f"ERROR GENERATE==>", e)

def check(state:State) -> dict:
    log.debug("======= PEMANGGILAN CHECK =========")
    try :
        cases = state["hasil"].test_cases
        masalah = []

        # rekayasa masalah
        # if state["percobaan"] < 2 :
        #     masalah.append("Judul setiap test case harus diawali kata nama fitur capslok menggunakan kurung siku")

        if state["project_id"] == "111" and not any(tc.type=="negative" for tc in cases):
            masalah.append("Belum ada test case negative")
        if any(len(tc.steps) > 5 for tc in cases):
            masalah.append("Ada test case yang memiliki steps yang lebih dari 5 langkah")
        log.debug(f"masalah muncul : {masalah}")
        
        return {"masalah": masalah} 

    except Exception as e:
        log.error(f"ERROR CHECK==>", e)
        raise e

def putuskan(state:State) -> dict :
    try:
        log.debug("======= PEMANGGILAN PUTUSKAN =========")
        if not state["masalah"]:
            return "selesai"
        if state["percobaan"] >= MAX_PERCOBAAN:
            return "menyerah"
        return "ulangi"
    except Exception as e:
        log.error(f"ERROR PUTUSKAN==>", e)

_graph = StateGraph(State)
_graph.add_node("generate",generate)
_graph.add_node("check",check),
_graph.add_edge(START, "generate")
_graph.add_edge("generate","check")
_graph.add_conditional_edges(
    "check", putuskan, {"ulangi": "generate", "menyerah": END, "selesai": END}
)
_app = _graph.compile()

def generate_test_cases(project_id: str, feature_description: str) -> TestCaseList:
    try:
        result = _agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": f"Project {project_id}. Buat test case untuk fitur: {feature_description}",
                    }
                ]
            },
            config={"callbacks": [LLMLogger()]}
        )
        # debug
        # print("============== INI UNTUK DEBUG =================")
        # for m in result["messages"]:
        #     m.pretty_print()
            
        return result["structured_response"]
    except Exception as e:
        log.error(f"ERROR GENERATE TEST CASE==>", e)

def run_graph(project_id: str, feature_description:str) -> TestCaseList:
    result = _app.invoke({
        "project_id": project_id,
        "feature_description": feature_description,
        "masalah": [],
        "percobaan": 0,
    })

    # if result["masalah"]:
    #     raise ValueError(
    #         f"Ada masalah di percobaan : {result["percobaan"]}"
    #     )
    

    log.debug(f"Selesai di percobaan ke {result["percobaan"]}")
    return result["hasil"]