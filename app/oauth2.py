from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from sqlmodel import select

from app import models
from .config import settings
from .token_schema import TokenData 
from .database import SessionDep


# OAuth2PasswordBearer automatically raises an HTTP 401 exception with the detail "Not authenticated"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings. secret_key
ALGORITHM = settings. algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings. access_token_expire_minutes

def create_access_token(data: dict):
    to_encode=data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
def verify_access_token(token:str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        id: int=payload.get("user_id")
        if id is None:
            raise credentials_exception

        token_data=TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    return token_data



def get_current_user(session:SessionDep,token:str =Depends(oauth2_scheme)):
    token=verify_access_token(token)
    statement= select(models.User).where(models.User.id==token.id)
    user= session.exec(statement).first()
    return user
