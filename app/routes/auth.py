from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from app.schemas.user import UserCreate, UserOut, LoginSchema, RefreshRequest
from app.db.database import get_session
from app.auth_service.auth_service import create_user, login_user, refresh_token
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.refresh_token import RefreshToken

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserOut)
async def signup(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await create_user(user, session)

@router.post("/login")
async def login(user: LoginSchema, session: AsyncSession = Depends(get_session)):
    return await login_user(user, session)

@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/refresh")
async def refresh(data: RefreshRequest, session: AsyncSession = Depends(get_session)):
   return await refresh_token(data, session)

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    await session.execute(
        delete(RefreshToken).where(RefreshToken.user_id == current_user.id)
    )
    await session.commit()
    return {
        "message": "Logged out"
    }
