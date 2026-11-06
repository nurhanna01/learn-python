from fastapi import FastAPI
from service import getLead
from models import Request,Response
import logging
from logger import correlation_id_var, setup_logging_tracer
import uuid

setup_logging_tracer()

app = FastAPI()

@app.middleware("http")
async def tambah_correlation_id(request, call_next):
    id = request.headers.get("Correlation-ID") or str(uuid.uuid4())
    correlation_id_var.set(id)
    response = await call_next(request)
    response.headers["Correlation-ID"] = id
    return response

log = logging.getLogger(__name__)
@app.post("/mr-review", response_model=Response)
def chat(req: Request):
    try:
        log.info("Hit api /mr-review")
        # Code yang mau direview
        MR_LIST = {
             "1" : '''
             def login(user, pw):
                q = "SELECT * FROM users WHERE name='" + user + "' AND pw='" + pw + "'"
                return db.execute(q)
                ''',
            "2" : '''
                import requests
                API_KEY = "sk-live-9f8a7b6c5d4e3f2a1b0c"
                def upload_data(data):
                    return requests.post(
                        "https://api.com/post",
                        headers={"Authorization": f"Bearer {API_KEY}"},
                        json=data,
                    )
                '''
        }

        code = MR_LIST.get(req.mr_id)
        
        result = getLead(code)
        return Response(data= result.structured_output)
    except Exception as e:
          log.error(f"Terjadi error : {e}")
          raise e