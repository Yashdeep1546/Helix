from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel
#==========================================
# USER SCHEMAS
# ==========================================
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True)

class UserCreate(UserBase):
    password: str  

class UserResponse(SQLModel):
    id: int
    email: EmailStr 
    model_config = {"from_attributes": True} 

class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserLogin(SQLModel):
    email:EmailStr
    password:str