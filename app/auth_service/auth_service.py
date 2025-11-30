from datetime import timedelta

from core.security import get_pass_hash, verify_pass_hash, create_access_token, create_refresh_token, decode_access_token
from fastapi import HTTPException, status
from models.user import User
from schemas.user import UserCreate, UserOut, LoginSchema, RefreshRequest
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.refresh_token import store_refresh_token
from models.refresh_token import RefreshToken

async def create_user(data: UserCreate, db: AsyncSession) -> UserOut:
    stmt = select(User).where(User.email == data.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # hash_password
    hashed_password = get_pass_hash(data.password)

    # create new user
    new_user = User(email=data.email, hashed_password=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return UserOut.model_validate(new_user)
    # return new_user

async def login_user(data: LoginSchema, db: AsyncSession):
    stmt = select(User).where(User.email == data.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(400, "Invalid email or password")

    # verify password
    if not verify_pass_hash(data.password, user.hashed_password):
        raise HTTPException(400, "Invalid email and password")

    # create JWT
    token = create_access_token({"sub": str(user.id)}, expires_delta=timedelta(minutes=1))
    refresh_token = create_refresh_token({"sub": str(user.id)}, expires_delta=timedelta(days=7))

    # store refresh token in db
    await store_refresh_token(user.id, refresh_token, db)

    return {
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


async def refresh_token(data: RefreshRequest, db: AsyncSession):
    refresh_token = data.refresh_token
    try:
        payload = decode_access_token(refresh_token)
        user_id = payload.get("sub")
    except:
        raise HTTPException(401, "Invalid refresh token")

    # delete's old refresh token
    await db.execute(
        delete(RefreshToken).where(RefreshToken.user_id == user_id)
    )

    new_access_token = create_access_token({"sub": str(user_id)}, expires_delta=timedelta(hours=30))
    new_refresh_token = create_refresh_token({"sub": str(user_id)}, expires_delta=timedelta(days=7))

    await store_refresh_token(user_id, new_refresh_token, db)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }
