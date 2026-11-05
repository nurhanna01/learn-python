from fastapi import FastAPI
from service import getLead
from models import Request,Response
import logging
from logger import logger_setup

logger_setup()
app = FastAPI()
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
                def login(user, password):
                    q = "SELECT * FROM users WHERE name='" + user + "' AND pw='" + pw + "'"
                    return db.execute(q)
                '''
        }
        code = MR_LIST.get(req.mr_id)
        
        data = getLead(code)
        return Response(message=data)
    except Exception as e:
          log.error(f"Terjadi error : {e}")
          raise e