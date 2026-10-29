from typing import Literal
from pydantic import BaseModel, Field

class TestCase(BaseModel):
    title: str = Field(description="Judul singkat test case")
    steps: list[str] = Field(min_length=1, description="Langkah berurutan")
    expected_result: str
    priority: Literal["low", "medium", "high"] = "medium"
    type: Literal["positive", "negative"]

class TestCaseList(BaseModel):
    test_cases: list[TestCase]

class GenerateRequest(BaseModel):
    feature_description: str = Field(min_length=3,description="Deskripsi fitur yang akan dites")
    project_id : Literal["111","222"] = Field(description="Project id")