from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from models.user import User
from schemas.user import UserCreate, UserOut
from core.security import get_pass_hash

async def create_user(data: UserCreate, db: AsyncSession) -> UserOut:
    stmt = select(User).where(User.email == data.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # hash_password
    hashed_password = get_pass_hash(data.password)

    # create new user
    new_user = User(email=data.email, hashed_password=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return UserOut.from_orm(new_user)
