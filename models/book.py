from sqlalchemy import String, Integer, UUID
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from database.session import Base

class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    release_year: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, default="наявна")