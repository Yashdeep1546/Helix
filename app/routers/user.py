from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from pwdlib import PasswordHash
from sqlmodel import select
from app.database import SessionDep
from app.models import User
from app.user_schema import UserCreate, UserUpdate, UserResponse

password_hash = PasswordHash.recommended()

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# ==========================================
# USER ENDPOINTS
# ==========================================
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, session: SessionDep):
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail={
                "message": "Email already registered"
            }
        )
    user.password=password_hash.hash(user.password)
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserResponse])
def get_all_users(session: SessionDep,limit:int=10,offset:int=0):
    statement=select(User).limit(limit).offset(offset)
    return session.exec(statement).all()

@router.get("/{id}", response_model=UserResponse)
def get_user_by_id(id: int, session: SessionDep):
    user = session.get(User, id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/{id}", response_model=UserResponse)
def update_user(user: UserUpdate, id: int, session: SessionDep):
    db_user = session.get(User, id)  
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_update = user.model_dump(exclude_unset=True)
    if "password" in user_update and user_update["password"] is not None:
        user_update["password"] = password_hash.hash(user_update["password"])
    db_user.sqlmodel_update(user_update)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/{id}")
def delete_user(id: int, session: SessionDep):
    db_user = session.get(User, id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    session.delete(db_user)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
