from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str):
    return ctx.hash(password)

def verify_password(password: str, hashed_password: str):
    return ctx.verify(password,hashed_password)

