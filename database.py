from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

engine = create_async_engine(settings.database_url)

# 비동기 세션 생성을 위한 sessionmaker 설정
AsyncSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
)

Base = declarative_base()

async def get_db() -> AsyncSession:
    """FastAPI 의존성 주입을 위한 데이터베이스 세션 생성기"""
    async with AsyncSessionLocal() as session:
        yield session
