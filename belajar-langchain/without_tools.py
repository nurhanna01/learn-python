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

gemini_model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash"
)
structured_model = gemini_model.with_structured_output(TestCase) 

result = structured_model.invoke("Buat satu test case untuk fitur login")
print("Title    :", result.title)
print("Steps    :", result.steps)
print("Expected :", result.expected_result)
print("Priority :", result.priority)
print("Notes    :", result.notes)