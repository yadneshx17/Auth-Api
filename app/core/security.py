from passlib.context import CryptContext

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_pass_hash(plain_password: str):
    return pwd_context.hash(plain_password)

def verify_pass_hash(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# JWT handling
