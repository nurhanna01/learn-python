import logging
from langchain_core.callbacks import BaseCallbackHandler
import json

log = logging.getLogger(__name__)

def logger_setup() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
    )

class LLMLogger(BaseCallbackHandler):
    def on_llm_end(self, response, **kwargs):
        msg = response.generations[0][0].message
        log.info(json.dumps({
            "model": msg.response_metadata.get("model_name"),
            "usage": msg.usage_metadata,
            "finish_reason": msg.response_metadata.get("finish_reason"),
        }, default=str, ensure_ascii=False))

    def on_llm_error(self, error, **kwargs):
        log.error("LLM error: %s", error)