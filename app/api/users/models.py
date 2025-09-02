from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    resumes = relationship(
        "Resumes",
        back_populates="user",
        cascade="all, delete-orphan",  # добавлено для каскадного удаления
    )

    def __str__(self):
        return f"Пользователь {self.email}"
