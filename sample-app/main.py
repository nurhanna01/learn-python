from fastapi import FastAPI, HTTPException
from models import GenerateRequest, TestCaseList
from generator_mercury import run_graph
from logger import logger_setup
import logging

app = FastAPI()

logger_setup()
log = logging.getLogger(__name__)

@app.post("/generate-test-cases", response_model=TestCaseList)
def generate(body: GenerateRequest):
    try:
        log.info("Mulai proses endpoint /generate-test-cases")
        return run_graph(body.project_id, body.feature_description)
    except Exception as e:
        log.error(f"error: {e}")
        raise HTTPException(status_code=500)