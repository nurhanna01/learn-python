from fastapi import FastAPI, HTTPException
from models import GenerateRequest, TestCaseList
from generator_mercury import generate_test_cases

app = FastAPI()

@app.post("/generate-test-cases", response_model=TestCaseList)
def generate(body: GenerateRequest):
    try:
        return generate_test_cases(body.project_id, body.feature_description)
    except Exception as e:
        raise HTTPException(status_code=503, detail="Layanan AI sedang sibuk")