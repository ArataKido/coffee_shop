from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.types import DateTime, Boolean, Integer
from datetime import datetime, timezone
from typing import Optional



class BaseModel(DeclarativeBase):
    """Base model for all entities in the system."""
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    
    # Audit fields
    created_by: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    updated_by: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Soft delete
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
