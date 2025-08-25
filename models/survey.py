from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    admin = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    entityName = Column(String(255), nullable=False)
    imageUrl = Column(String(2048), nullable=False)
    captions = Column(JSON, nullable=False)
    approved = Column(Boolean, default=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())

    responses = relationship("Response", back_populates="survey")

class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"))
    respondent_id = Column(Integer, ForeignKey("users.db_id"))
    answers = Column(JSON, nullable=False)

    survey = relationship("Survey", back_populates="responses")
    respondent = relationship("User")
