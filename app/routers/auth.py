
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from pwdlib import PasswordHash
from sqlmodel import select

from fastapi import APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, models, user_schema,oauth2
from ..token_schema import Token

router = APIRouter(tags=["Authentication"])

@router.post("/login",response_model=Token)
def login(session:database.SessionDep,user_info: OAuth2PasswordRequestForm = Depends()):

   user = session.exec(select(models.User).where(models.User.email == user_info.username)).first()
   if user is None:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credential")
   
   password=PasswordHash.recommended().verify(user_info.password,user.password)

   if password is False:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credential")
   
   access_token = oauth2.create_access_token(data={"user_id": user.id})

   return {"access_token" : access_token, "token_type": "bearer"}
   
