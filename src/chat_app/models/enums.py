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


class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class MessageStatus(StrEnum):
    READING = "reading"
    GENERATING = "generating"
    VALIDATED = "validated"
    CONCLUDED = "concluded"
    FAILED = "failed"
    CANCELED = "canceled"


class UpdateError(StrEnum):
    INCORRECT = "Password incorrect"
    NOT_MATCH = "The provider passwords do not match"
    NOT_EXIST = "User Don't exists"