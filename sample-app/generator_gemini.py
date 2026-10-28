from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from models import TestCaseList

load_dotenv()

def get_test_standard(project_id: str) -> str:
    """Ambil standar penulisan test case untuk sebuah project.
    Panggil ini sebelum membuat test case supaya formatnya sesuai standar."""
    print(f"[TOOL DIPANGGIL] project_id={project_id}")
    standar = {
        "proj-a": "Setiap test case wajib punya skenario negatif. Langkah maksimal 5.",
        "proj-b": "Prioritas high hanya untuk alur pembayaran.",
    }
    return standar.get(project_id, "Standar tidak ditemukan untuk project ini")

# Dibuat sekali di level modul, bukan tiap dipanggil
_model = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

_agent = create_agent(
    model=_model,
    tools=[get_test_standard],
    response_format=TestCaseList,
    system_prompt="Kamu QA engineer. Ambil standar project dulu, lalu buat test case.",
)

def generate_test_cases(project_id: str, feature_description: str) -> TestCaseList:
    result = _agent.invoke(
        {"messages": [{"role": "user", "content": f"Project {project_id}. Buat test case untuk fitur: {feature_description}"}]}
    )
    return result["structured_response"]

