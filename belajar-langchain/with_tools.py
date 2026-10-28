from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field, ValidationError
from typing import Literal

load_dotenv()

class TestCase(BaseModel):
    title: str = Field(description="Judul singkat test case")
    steps: list[str] = Field(min_length=1, description="Langkah eksekusi berurutan")
    expected_result: str
    priority: Literal["low", "medium", "high"] = "medium"
    notes: str | None = None

class TestCaseList(BaseModel):
    test_cases: list[TestCase]

gemini_model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash"
)

def get_test_standard(project_id: str) -> str:
    """Ambil standar penulisan test case untuk sebuah project.
    Panggil ini sebelum membuat test case supaya formatnya sesuai standar."""
    print(f"[TOOL DIPANGGIL] project_id={project_id}")
    standar = {
        "proj-a": "Setiap test case wajib punya skenario negatif. Langkah maksimal 5.",
        "proj-b": "Prioritas high hanya untuk alur pembayaran.",
    }
    return standar.get(project_id, "Standar tidak ditemukan untuk project ini")

agent = create_agent(
    model=gemini_model,
    tools=[get_test_standard],
    response_format=TestCaseList,
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {
        "messages": [{"role": "user", "content": "Project proj-a. Buat test case untuk fitur login."}]
    }
)

hasil = result["structured_response"]
for tc in hasil.test_cases:
    print(tc.title, "|", tc.priority)