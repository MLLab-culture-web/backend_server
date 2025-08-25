from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    db_id = Column(Integer, primary_key=True, index=True)
    id = Column(String(8), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
