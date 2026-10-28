import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from models import TestCaseList

load_dotenv()

STANDARDS = {
        "proj-a": "Setiap test case wajib punya skenario negatif. Langkah maksimal 5.",
        "proj-b": "Prioritas high hanya untuk alur pembayaran.",
}

def get_test_standard(project_id: str) -> str:
    """Ambil standar penulisan test case untuk sebuah project.
    Panggil ini sebelum membuat test case supaya formatnya sesuai standar."""
    print(f"[TOOL DIPANGGIL] project_id={project_id}")
    return STANDARDS.get(project_id, "Standar tidak ditemukan untuk project ini")

_model = ChatOpenAI(
    model="mercury-3",
    api_key=os.environ["INCEPTION_API_KEY"],
    base_url="https://api.inceptionlabs.ai/v1",
    temperature=0.75,
)

_agent = create_agent(
    model=_model,
    tools=[get_test_standard],
    response_format=TestCaseList,
    system_prompt="Kamu QA engineer. Ambil standar project dulu, lalu buat test case.",
)


def generate_test_cases(project_id: str, feature_description: str) -> TestCaseList:
    result = _agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Project {project_id}. Buat test case untuk fitur: {feature_description}",
                }
            ]
        }
    )
    # debug
    for m in result["messages"]:
        m.pretty_print()
        
    return result["structured_response"]