from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index
from datetime import datetime
from sqlalchemy.sql import func

from app.db.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (Index("idx_user_token", "user_id", "token"),)

async def store_refresh_token(user_id: int, token: str, db) :
    db.add(RefreshToken(user_id=user_id, token=token))
    await db.commit()
