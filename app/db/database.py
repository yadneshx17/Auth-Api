from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
# import os
# from dotenv import load_dotenv
from config.settings import settings

# load environment vairables from .env file
# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

Async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

async def get_session():
    async with Async_session() as session:
        yield session
