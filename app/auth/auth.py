from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timedelta, timezone

from models.auth import Token
from operations.user_operations import get_user_by_name
from auth.security import verify_password

SECRET = "d698e8ea55b1352dabedc22b474a13f27a637b4e50c4decdf45965fb4354503e"
ALGORITHM = "HS256"
TOKEN_EXPIRY = 5

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(session:AsyncSession,user_name: str, password: str):
    user: dict = await get_user_by_name(session=session,username=user_name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )
    if not verify_password(password,hashed_password=user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to authenticate!!"
        )
    return user

def create_token(data: dict, expiry_delta: timedelta | None = None):
    data_copy = data.copy()
    if "sub" in data_copy:
        data_copy["sub"] = str(data_copy["sub"])

    if expiry_delta:
        expiry = datetime.now(timezone.utc) + expiry_delta
    else:
        expiry = datetime.now(timezone.utc) + timedelta(minutes=10)

    data_copy.update({"expires": expiry.isoformat()})
    token = jwt.encode(data_copy,key=SECRET,algorithm=ALGORITHM)

    return Token(access_token=token,token_type="bearer")

async def generate_token(
        session: AsyncSession,
        form_data: OAuth2PasswordRequestForm):
    user = await authenticate_user(
        session=session, user_name=form_data.username,
        password=form_data.password)
    if not user:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Incorrect username or password"
    )

    expiry_delta = timedelta(minutes=5)
    data = {"sub": user.get("id")}

    return create_token(data=data,expiry_delta=expiry_delta)

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
    
