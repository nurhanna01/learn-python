from fastapi import FastAPI, HTTPException
from models import GenerateRequest, TestCaseList
from generator_mercury import run_graph
from logger import logger_setup
import logging
import uuid
from correlation import correlation_id_var, setup_logging_tracer

setup_logging_tracer()

app = FastAPI()

@app.middleware("http")
async def tambah_correlation_id(request, call_next):
    id = request.headers.get("Correlation-ID") or str(uuid.uuid4())
    correlation_id_var.set(id)
    response = await call_next(request)
    response.headers["Correlation-ID"] = id
    return response

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