from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import schemas
import crud
from database import get_db
from utils.security import verify_password

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """회원가입 API"""
    existing_user = await crud.get_user_by_id(db, user_id=user_in.id)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 존재하는 아이디입니다.",
        )
    
    await crud.create_user(db=db, user=user_in)
    return {"message": "회원가입 성공"}

@router.post("/login")
async def login(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """로그인 API"""
    user = await crud.get_user_by_id(db, user_id=user_in.id)
    if not user or not verify_password(user_in.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="아이디 또는 비밀번호가 잘못되었습니다.",
        )

    return {"message": "로그인 성공", "user": {"id": user.id}}
