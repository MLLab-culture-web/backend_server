from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database import engine, Base
from routers import auth, survey
# SQLAlchemy 모델을 임포트하여 Base가 인식하도록 함
from models import user, survey as survey_model

app = FastAPI(
    title="CultureLens API with MySQL",
    description="Node.js Express 프로젝트를 FastAPI와 MySQL로 변환한 프로젝트입니다.",
    version="1.1.0"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """
    애플리케이션 시작 시, 데이터베이스 테이블을 생성합니다.
    """
    async with engine.begin() as conn:
        # 개발 중에는 기존 테이블을 삭제하고 다시 생성할 수 있습니다.
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["인증"])
app.include_router(survey.router, prefix="/survey", tags=["설문"])

@app.get("/", tags=["Root"])
async def read_root():
    """루트 경로, 서버의 상태를 확인하는 기본 엔드포인트입니다."""
    return {"message": "✅ 서버가 잘 작동 중입니다."}

# uvicorn 서버를 직접 실행하려면 아래 코드를 활성화하세요.
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
