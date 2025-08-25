from pydantic import BaseModel, constr
from typing import List, Optional
from datetime import datetime

# ====================
#       User
# ====================
class UserBase(BaseModel):
    id: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    db_id: int

    class Config:
        from_attributes = True

# ====================
#      Response
# ====================
class ResponseBase(BaseModel):
    answers: List[int]

class ResponseCreate(ResponseBase):
    respondent_id: int

class Response(ResponseBase):
    id: int
    survey_id: int
    respondent_id: int

    class Config:
        from_attributes = True

# ====================
#       Survey
# ====================
class SurveyBase(BaseModel):
    admin: str
    country: str
    category: str
    entityName: str
    imageUrl: str
    captions: List[str]
    approved: bool = False

class SurveyCreate(SurveyBase):
    pass

class Survey(SurveyBase):
    id: int
    createdAt: datetime
    responses: List[Response] = []

    class Config:
        from_attributes = True
