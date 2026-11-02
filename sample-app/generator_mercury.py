import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from models import TestCaseList
from typing import TypedDict
from langgraph.graph import StateGraph, END, START
from logger import logger_setup, LLMLogger
import logging
from gherkin_tool import write_gherkin, OUTPUT_DIR

logger_setup()
log = logging.getLogger(__name__)

load_dotenv()

STANDARDS = {
        "1": "Setiap test case wajib punya skenario negatif. Langkah minimal 3. Langkah maksimal 8.",
        "2": "Prioritas high hanya untuk alur pembayaran.",
}

MAX_ATTEMPS = 3

class State(TypedDict):
    project_id : str
    feature_description : str
    result : TestCaseList
    problem : str
    attempts : int


# def get_test_rule(project_id: str) -> str:
#     """Ambil standar penulisan test case untuk sebuah project.
#     Panggil ini sebelum membuat test case supaya formatnya sesuai standar."""
#     log.info(f"[TOOL DIPANGGIL] project_id={project_id}")
#     if project_id not in STANDARDS:
#         log.error(f"Project '{project_id}' tidak dikenal")
#         raise ValueError(f"Project '{project_id}' tidak dikenal")
#     return STANDARDS.get(project_id, "Standar tidak ditemukan untuk project ini")

_model = ChatOpenAI(
    model="mercury-3",
    api_key=os.environ["INCEPTION_API_KEY"],
    base_url="https://api.inceptionlabs.ai/v1",
    temperature=0.75,
)

_agent = create_agent(
    model=_model,
    tools=[],
    response_format=TestCaseList,
    system_prompt="Kamu QA engineer. Ambil aturan project dulu, lalu buat test case.",
)

def generate(state: State) -> dict :
    try:
        log.debug("============== PEMANGGILAN GENERATE ====================")
        log.debug(f"Mulai Percobaan ke =========================> {state.get("attempts") + 1}")
        deskripsi = state["feature_description"]
        if state.get("problem"):
            deskripsi += (
                "\nPerbaiki problem berikut dari percobaan sebelumnya: \n"
                + "".join(state["problem"])
            )
        log.debug(f"==PROMPT KE AI] percobaan ke {state.get("attempts") + 1} ==>>>>>>{deskripsi}")
        
        result = generate_test_cases(state["project_id"],deskripsi)
        attempts = state.get("attempts", 0) + 1
        log.debug(f"selesai generate percobaan ke {attempts},")

        return {"result":result, "attempts":attempts}
    except Exception as e:
        log.error(f"ERROR GENERATE==>{e}")
        raise e

def check(state:State) -> dict:
    log.debug("======= PEMANGGILAN CHECK =========")
    try :
        cases = state["result"].test_cases
        problem = []

        # rekayasa problem
        # if state["attempts"] < 2 :
        #     problem.append("Judul setiap test case harus diawali kata nama fitur capslok menggunakan kurung siku")

        if state["project_id"] == "1" and not any(tc.type=="negative" for tc in cases):
            problem.append("Belum ada test case negative")
        if any(len(tc.steps) > 8 for tc in cases):
            problem.append("Ada test case yang memiliki steps yang lebih dari 8 langkah")
        log.debug(f"problem muncul : {problem}")
        
        return {"problem": problem} 

    except Exception as e:
        log.error(f"ERROR CHECK==> {e}")
        raise e

def decide (state:State) -> dict :
    try:
        log.debug("======= PEMANGGILAN decide  =========")
        if not state["problem"]:
            return "complete"
        if state["attempts"] >= MAX_ATTEMPS:
            return "give_up"
        return "retry"
    except Exception as e:
        log.error(f"ERROR decide ==>{e}")
        raise e

_writer_agent = create_agent(
    model=_model,
    tools=[write_gherkin],
    system_prompt="""Ubah test case yang saya berikan ke dalam gherkin file.
    Gunakan format best practise dengan format menggunakan english tapi jangan mengubah-ubah isi test case.
    Simpan ke dalam file md"""
)

def store(state: State) -> dict:
    log.debug("======= PEMANGGILAN STORE =========")
    try:
        filename = f"{state['project_id']}.md"
        target = OUTPUT_DIR / filename

        _writer_agent.invoke({
            "messages": [{
                "role": "user",
                "content": (
                    f"filename: {filename}\n"
                    f"fitur: {state['feature_description']}\n"
                    f"test cases:\n{state['result'].model_dump_json()}"
                ),
            }]
        })

        if not target.exists():
            raise RuntimeError("AI tidak memanggil write_gherkin, file tidak dibuat")
        log.info(f"File tersimpan di: {target}")
        return {}
    except Exception as e:
        log.error(f"ERROR STORE==> {e}")
        raise e

_graph = StateGraph(State)
_graph.add_node("generate",generate)
_graph.add_node("check",check),
_graph.add_node("store",store),
_graph.add_edge(START, "generate")
_graph.add_edge("generate","check")
_graph.add_conditional_edges(
    "check", decide , {"retry": "generate", "give_up": END, "complete": "store"}
)
_graph.add_edge("store",END)
_app = _graph.compile()

def generate_test_cases(project_id: str, feature_description: str) -> TestCaseList:
    try:
        result = _agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": f"Project {project_id}. Buat test case untuk fitur: {feature_description} dengan aturan {STANDARDS.get(project_id, "Standar tidak ditemukan untuk project ini")}",
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
        log.error(f"ERROR GENERATE TEST CASE==>{e}")
        raise e

def run_graph(project_id: str, feature_description:str) -> TestCaseList:
    result = _app.invoke({
        "project_id": project_id,
        "feature_description": feature_description,
        "problem": [],
        "attempts": 0,
    })

    # if result["problem"]:
    #     raise ValueError(
    #         f"Ada problem di percobaan : {result["attempts"]}"
    #     )
    

    log.info(f"Selesai di percobaan ke {result["attempts"]}")
    return result["result"]