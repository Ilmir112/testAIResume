
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class ResumesHistory(Base):
    __tablename__ = "resumes_history"

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)
    context = Column(Text)

    resume = relationship("Resumes", back_populates="histories")


class Resumes(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String, nullable=False)
    context = Column(Text, nullable=False)

    user = relationship("Users", back_populates="resumes")
    histories = relationship(
        "ResumesHistory",
        back_populates="resume",
        cascade="all, delete-orphan",  # добавлено для каскадного удаления историй
    )
