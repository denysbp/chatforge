from dataclasses import dataclass

@dataclass(frozen=True)
class Enviroment:
    OPENIA_API: str
    ADMIN_LOGIN: str
    ADMIN_PASSWORD: str
    PORT: int
    DB_NAME: str
    DB_PASSWORD: str
    DB_URL: str
    SECRECT_KEY: str
    ACESS_TOKEN_EXPIRE_MINUTES: int
