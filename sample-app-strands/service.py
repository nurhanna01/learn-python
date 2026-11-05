from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands.models.openai import OpenAIModel
import os
from dotenv import load_dotenv
from models import AgentReview, LeadDecision
import logging
from logger import logger_setup

logger_setup()
log = logging.getLogger(__name__)

# _model = OllamaModel(host="http://localhost:11434", model_id="llama3.1")
load_dotenv()

_model_mercury = OpenAIModel(
    client_args = {
        "api_key": os.environ["INCEPTION_API_KEY"],
        "base_url": "https://api.inceptionlabs.ai/v1",
    },
    model_id="mercury-3"
    )

@tool
def securityReview(code:str)->str:
    """"Kamu adalah agent security yang memastikan semua code aman dari masalah security. Pakai Bahasa Indonesia"""
    log.info(f"======PEMANGGILAN TOOL AGENT SECURITY====")
    _security_agent = Agent(
        model=_model_mercury,
        system_prompt=f"""Kamu agent yang hanya fokus pada masalah security.
        - kamu harus memberikan salinan code yang bermasalah.
        - Jelaskan masalah untuk kode tersebutn dengan ringkas.
        - Lalu berikan solusi untuk menghindari masalah tersebut. 
        - Buatkan code yang sudah diperbaiki terhadapa masalah tersebut.
        - Jika kamu tidak mampu jangan mengarang, katakan tidak mampu dan sebutkan alasan kenapa kamu tidak mampu.
        """,
        structured_output_model=AgentReview
    )
    _result = _security_agent(f"Kode yang harus di review : {code}")
    return f"hasil review agent security : {_result}"

@tool
def developerReview(code:str)->str:
    """"Kamu adalah agent developer yang memastikan semua code ditulis dengan gaya penulisan konsisten. Pakai Bahasa Indonesia"""
    log.info(f"======PEMANGGILAN TOOL AGENT DEVELOPER====")
    _developer_agent = Agent(
        model=_model_mercury,
        system_prompt=f"""Kamu agent yang ahli dalam penulisan code.
        - kamu hanya mereview kode berdasarkan gaya penulisan yang sesuai best practise.
        - Code harus bersih dari comment yang bukan bersifat dokumentasi, menggunakan bahasa yang konsisten, menggunakan nama variabel yang punya makna terhadap manfaatnya.
        - Berikan potongan kode yang bermasalah.
        - Jelaskan masalah dengan ringkas.
        - Lalu berikan solusi untuk menghindari masalah tersebut. 
        - Berikan juga code yang sudah diperbaiki agar bisa diikuti user.
        - Jika kamu tidak mampu jangan mengarang, katakan tidak mampu dan sebutkan alasan kenapa kamu tidak mampu.
        """,
        structured_output_model=AgentReview
    )
    _result = _developer_agent(f"Kode yang harus di review : {code}")
    return f"hasil review agent developer : {_result.message}"

def getLead(code :str)-> Agent:
    log.info(f"======PEMANGGILAN AGENT LEAD====")
    _lead_agent = Agent(
        model=_model_mercury,
        tools=[securityReview, developerReview],
        system_prompt=f"""Kamu adalah tech lead yang akan memerintahkan agent lain untuk review dari kode yang diberikan. Pakai Bahasa Indonesia.
        Kamu menuruuh agent lain untuk review.
        Masalah sequrity = tugas  agent security untuk mereview.
        Maslah penulisan code = tugas agent developer untuk mereview.
        jika agent tidak mampu menemukan masalah dan agent meminta bantuanmu, maka kamu sendiri yang meriew bagian tersebut.
        Kamu dapat menerima atau menolak hasil review masing-masing agent sesuai dengan pengetahuanmu.
        Berikut adalah code yang perlu kamu perintahkan mereka untuk review {code}""",
        structured_output_model=LeadDecision
    )
    _result = _lead_agent(f"Kode yang harus di review : {code}")
    return _result.message

