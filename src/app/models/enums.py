from enum import StrEnum, auto

class EnvErrorType(StrEnum):
    NOT_EXIST = auto()
    INVALID = auto()
    MISSING = auto()


class LogLevels(StrEnum):
    warn = "WARN"
    info = "INFO"
    error = "ERROR"
    debug = "DEBUG"
