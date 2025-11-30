from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from models.refresh_tokens import RefreshToken

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

async def store_refresh_token(user_id: int, token: str, db) :
    db.add(RefreshToken(user_id=user_id, token=token))
    await db.commit()
