from typing import Literal
from pydantic import BaseModel, Field

class TestCase(BaseModel):
    title: str = Field(description="Judul singkat test case")
    steps: list[str] = Field(min_length=1, description="Langkah berurutan")
    expected_result: str
    priority: Literal["low", "medium", "high"] = "medium"

class TestCaseList(BaseModel):
    test_cases: list[TestCase]

class GenerateRequest(BaseModel):
    feature_description: str = Field(description="Deskripsi fitur yang akan dites")
    project_id : str = Field(description="Project id")