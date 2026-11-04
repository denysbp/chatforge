from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..enviroment import ensure_env, Enviroment
import sys
from ..models import Base
from .. import models

class DataBase:
    def __init__(self):
        env = ensure_env()
        if not isinstance(env, dict):
            sys.exit(1)
        data = Enviroment(**env)
        connection = f"{data.DB_URL}{data.DB_NAME}"
        self.engine = create_engine(
            connection,
            echo=True,
            pool_pre_ping=True
        )
        self.SessionLocal = sessionmaker(
            bind=self.engine,
        )

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

    def close(self):
        self.engine.dispose()