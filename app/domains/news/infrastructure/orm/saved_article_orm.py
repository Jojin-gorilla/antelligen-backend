from datetime import datetime

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base


class SavedArticleOrm(Base):
    __tablename__ = "saved_article"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    link: Mapped[str] = mapped_column(Text, nullable=False)
    link_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    published_at: Mapped[str | None] = mapped_column(String(100), nullable=True)
    snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    saved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
