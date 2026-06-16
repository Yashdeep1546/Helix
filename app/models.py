from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, DateTime, func
from app.post_schema import PostBase
from app.user_schema import UserBase
from sqlmodel import Field


# ==========================================
# POST MODEL
# ==========================================
class Post(PostBase, table=True):
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    owner_id:int =Field(foreign_key="users.id",ondelete="CASCADE")
    owner: "User" = Relationship(back_populates="posts")


# ==========================================
# USER MODEL
# ==========================================
class User(UserBase, table=True):  #  Fixed: Added table=True
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str  
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    posts: List["Post"] = Relationship(back_populates="owner")



# ==========================================
# VOTE MODEL
# ==========================================
class Vote(SQLModel, table=True):
    __tablename__ = "votes"

    user_id: int = Field(
        foreign_key="users.id", 
        ondelete="CASCADE", 
        primary_key=True
    )
    post_id: int = Field(
        foreign_key="posts.id", 
        ondelete="CASCADE", 
        primary_key=True
    )
