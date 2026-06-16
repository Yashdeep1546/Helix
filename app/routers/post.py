from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlmodel import select
from app import oauth2
from app.database import SessionDep
from app.models import Post, Vote
from app.post_schema import PostCreate, PostUpdate, PostResponse,PostWithVotesResponse

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# ==========================================
# POST ENDPOINTS
# ==========================================
@router.get("/", response_model=List[PostWithVotesResponse])
def get_posts(session: SessionDep,limit:int=10,offset:int=0):
    statement = (
        select(Post, func.count(Vote.post_id).label("votes"))
        .outerjoin(Vote, Post.id == Vote.post_id)
        .group_by(Post.id)
        .limit(limit)
        .offset(offset)
    )
    posts = session.exec(statement).all()
    return posts

@router.get("/{id}", response_model=PostWithVotesResponse)
def get_post(id: int, session: SessionDep):
    statement = (
        select(Post, func.count(Vote.post_id).label("votes"))
        .outerjoin(Vote, Post.id == Vote.post_id)
        .where(Post.id == id)
        .group_by(Post.id)
    )
    post = session.exec(statement).first()
    if post is None or post[0] is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, session: SessionDep,current_user=Depends(oauth2.get_current_user)):
    db_post = Post.model_validate(post,update={"owner_id":current_user.id})
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: PostUpdate, session: SessionDep,current_user=Depends(oauth2.get_current_user)):

    
    db_post = session.get(Post, id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if current_user.id!=db_post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not your post")

    
    post_update = post.model_dump(exclude_unset=True)
    db_post.sqlmodel_update(post_update)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@router.delete("/{id}")
def delete_post(id: int, session: SessionDep,current_user=Depends(oauth2.get_current_user)):
    
    
    db_post = session.get(Post, id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if current_user.id!=db_post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not your post")
    
    session.delete(db_post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
