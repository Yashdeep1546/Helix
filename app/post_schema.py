from typing import Optional
from sqlmodel import  SQLModel
from app.user_schema import UserResponse
# ==========================================
# POST SCHEMAS
# ==========================================
class PostBase(SQLModel):
    title: str
    content: str
    published: bool = True
    model_config = {"from_attributes": True}

class PostCreate(PostBase):
    pass

class PostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class PostResponse(SQLModel):
    id: int  
    title: str
    content: str
    published: bool
    owner_id :int
    owner:UserResponse

class PostWithVotesResponse(SQLModel):
    Post: PostResponse
    votes: int
