from db.database import Base
from sqlalchemy  import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    # username in migration
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
