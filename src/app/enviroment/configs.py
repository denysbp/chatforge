from dotenv import load_dotenv
from pathlib import Path
from ..models import (
    EnvErrorType,
    LogLevels
)
import logging
import os

ENV_KEYS = [
    "OPENIA_API",
    "ADMIN_LOGIN",
    "ADMIN_PASSWORD",
    "PORT",
    "DB_NAME",
    "DB_PASSWORD",
    "DB_URL",
    "SECRECT_KEY",
    "ALGORITHM",
    "ACESS_TOKEN_EXPIRE_MINUTES",
]

ENV_PATH = Path(".env")
EXAMPLE = Path(".env.example")
DEFAULT_MESSAGE = "change-me"


def create_env() -> None:
    try:
        with EXAMPLE.open("w", encoding="utf-8") as file:
            string = ""
            for key in ENV_KEYS:
                string += f"{key} = '{DEFAULT_MESSAGE}'\n"
            file.write(string)
    except IOError as e:
        logging.warning(e)

def ensure_env() -> str:
    load_dotenv()
    if not ENV_PATH.exists() and not ENV_PATH.is_file():
        create_env()
        logging.warning(
            "Credentials not defined, "
            "we have created .env.example.\n"
            "Copy the keys."
            "Change the credentials and launch "
            "the program again"
        )
        return EnvErrorType.NOT_EXIST
    try:
        with ENV_PATH.open("r", encoding="utf-8") as file:
            text = file.read()
            if not text:
                logging.warning(
                    ".env is empty!"
                )
                create_env()
                return EnvErrorType.INVALID
            values = [os.getenv(key) for key in ENV_KEYS]
            if any(key is None for key in values):
                logging.warning(
                    "we decteted missing values on .env"
                )
                return EnvErrorType.MISSING
            if any(value == DEFAULT_MESSAGE for value in values):
                logging.warning(
                    "You need to pass values on your .env "
                    "file default messages can't be used."
                )
                return EnvErrorType.INVALID
    except PermissionError:
        logging.info(
            "we don't have acess to .env file "
            "not permission error."
        )

if __name__ == "__main__":
    ensure_env()
