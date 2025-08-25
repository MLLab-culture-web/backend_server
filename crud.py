from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import user as models_user, survey as models_survey
from schemas import UserCreate, SurveyCreate, ResponseCreate
from utils.security import get_password_hash

# ====================
#       User
# ====================
async def get_user_by_id(db: AsyncSession, user_id: str):
    """ID로 사용자를 조회합니다."""
    result = await db.execute(select(models_user.User).filter(models_user.User.id == user_id))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate):
    """새로운 사용자를 생성합니다."""
    hashed_password = get_password_hash(user.password)
    db_user = models_user.User(id=user.id, password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# ====================
#       Survey
# ====================
async def create_survey(db: AsyncSession, survey: SurveyCreate) -> models_survey.Survey:
    """새로운 설문을 생성합니다."""
    db_survey = models_survey.Survey(**survey.model_dump())
    db.add(db_survey)
    await db.commit()
    await db.refresh(db_survey)
    return db_survey

async def get_surveys(db: AsyncSession, skip: int = 0, limit: int = 100):
    """전체 설문 목록을 조회합니다."""
    result = await db.execute(select(models_survey.Survey).offset(skip).limit(limit).order_by(models_survey.Survey.createdAt.desc()))
    return result.scalars().all()

async def get_survey(db: AsyncSession, survey_id: int):
    """ID로 특정 설문을 조회합니다."""
    result = await db.execute(select(models_survey.Survey).filter(models_survey.Survey.id == survey_id))
    return result.scalars().first()

# ====================
#      Response
# ====================
async def create_survey_response(db: AsyncSession, response: ResponseCreate, survey_id: int):
    """설문에 대한 응답을 생성합니다."""
    db_response = models_survey.Response(**response.model_dump(), survey_id=survey_id)
    db.add(db_response)
    await db.commit()
    await db.refresh(db_response)
    return db_response
