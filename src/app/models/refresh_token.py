from sqlalchemy import (
    DateTime,
    UUID,
    String,
    ForeignKey
)
from uuid import uuid4
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    
)
from datetime import (
    datetime,
    timezone
)

class RefreshToken:
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda : uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    token_hash: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default= datetime.now(timezone.utc)
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    revoked_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )