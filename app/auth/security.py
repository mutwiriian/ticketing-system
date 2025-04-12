from typing import Annotated

from fastapi import Depends, HTTPException

import jwt
from jwt.exceptions import InvalidTokenError

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET = "d698e8ea55b1352dabedc22b474a13f27a637b4e50c4decdf45965fb4354503e"
ALGORITHM = "HS256"
TOKEN_EXPIRY = 5

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str):
    return ctx.hash(password)

def verify_password(password: str, hashed_password: str):
    return ctx.verify(password,hashed_password)

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)]
) -> int:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(token,key=SECRET,algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        if user_id is None:
            raise credential_exception
        return int(user_id)
    except InvalidTokenError:
        raise credential_exception

