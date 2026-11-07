from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..enviroment import ensure_env, settings
import sys
from ..models import Base
from .. import models
from typing import Generator


class DataBase:
    def __init__(self):
        self.engine = create_engine(
            settings.DB_URL.encoded_string(),
            pool_pre_ping=True
        )
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False
        )

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def get_db(self) -> Generator[Session]:
        with self.SessionLocal() as db:
            yield db

    def close(self):
        self.engine.dispose()

    def drop_tables(self):
        Base.metadata.drop_all(bind=self.engine)

data_base = DataBase()
data_base.create_tables()