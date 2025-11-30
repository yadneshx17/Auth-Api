from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from config.settings import settings

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_pass_hash(plain_password: str):
    return pwd_context.hash(plain_password)

def verify_pass_hash(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# JWT handling
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    # expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=setttings.access_token_expire_minutes))

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        settings.jwt_algorithm
    )

    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire})

    encoded_token = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        json_encoder=None,  # REMOVE custom encoder
    )
    return encoded_token

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            settings.jwt_algorithm
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            settings.jwt_algorithm
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Refresh token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid refresh token")
