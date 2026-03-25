from datetime import datetime

from sqlalchemy import String, Text, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base


class BoardOrm(Base):
    __tablename__ = "board"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    account_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
