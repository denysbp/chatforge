import logging
from src.chat_app.models import LogLevels

DEBUG_FORMAT = (
    "%(levelname)s:%(message)s:"
    "%(pathname)s:%(funcName)s:%(lineno)d"
)


def configure_logging(
    log_level: str | LogLevels = LogLevels.error
) -> None:

    if isinstance(log_level, LogLevels):
        log_level = log_level.value

    log_level = str(log_level).upper()

    valid_levels = [level.value for level in LogLevels]

    if log_level not in valid_levels:
        log_level = LogLevels.error.value

    logging.basicConfig(
        level=log_level,
        format=DEBUG_FORMAT if log_level == "DEBUG"
        else "%(levelname)s:%(message)s"
    )