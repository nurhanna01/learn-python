import logging
from contextvars import ContextVar

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="-")


def add_correlation_id(record: logging.LogRecord) -> bool:
    record.correlation_id = correlation_id_var.get()
    return True


def setup_logging_tracer() -> None:
    logging.basicConfig(
        format="%(asctime)s [%(correlation_id)s] %(levelname)s %(name)s: %(message)s",
        force=True,
        level=logging.INFO,
    )
    # supaya log dari SEMUA logger ikut kena
    for handler in logging.getLogger().handlers:
        handler.addFilter(add_correlation_id)