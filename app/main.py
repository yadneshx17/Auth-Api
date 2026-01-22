from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.models.user import User
from app.routes.auth import router as auth_router


# Create tables asynchronously
async def init_models():
    async with engine.begin() as conn:
        print("Table creating")
        await conn.run_sync(Base.metadata.create_all)
        print("Table Created")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Started")
    await init_models()
    yield
    print("Shutting down")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.google.com"],
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(auth_router)

@app.get("/ping")
def ping():
    return {"message": "pong"}
