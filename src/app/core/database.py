from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..enviroment import ensure_env, settings
import sys
from ..models import Base
from .. import models


class DataBase:
    def __init__(self):
        self.engine = create_engine(
            settings.DB_URL.encoded_string(),
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

    def drop_tables(self):
        Base.metadata.drop_all(bind=self.engine)