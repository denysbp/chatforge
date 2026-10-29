from app import LogLevels
import logging


DEBUG_FORMAT = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


def configure_logging(log_level: str = LogLevels.error) -> None:
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels]

    if log_level not in log_levels:
        logging.basicConfig(level=LogLevels.error)
        return

    if log_level == LogLevels.debug:
        logging.basicConfig(level=LogLevels.debug, format=DEBUG_FORMAT)
        return

    logging.basicConfig(level=log_level)
