from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate, UserOut
from db.database import get_session
from auth_service.auth_service import create_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserOut)
async def signup(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await create_user(user, session)
