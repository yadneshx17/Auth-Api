from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt

from core.security import decode_access_token
from db.database import get_session
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)
):
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token expired"
        )

    stmt = select(User).where(User.id == int(user_id))
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(401, "User not found")

    return user
