from sqlalchemy import (
    ForeignKey,
    String
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import Base


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(30))