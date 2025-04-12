from passlib.context import CryptContext

ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return ctx.hash(password)

def verify_password(password: str, hashed_password: str):
    return ctx.verify(password,hashed_password)


