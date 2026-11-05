import logging

log = logging.getLogger(__name__)

def logger_setup() -> None:
    logging.basicConfig(
        format="%(asctime)s [] %(levelname)s %(name)s: %(message)s",
        level=logging.INFO,
    )