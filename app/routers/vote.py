from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from app import oauth2, models
from app.database import SessionDep
from app import vote_schema

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: vote_schema.Vote, 
    session: SessionDep, 
    current_user=Depends(oauth2.get_current_user)
):
    post = session.get(models.Post, vote.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {vote.post_id} does not exist"
        )

    statement = select(models.Vote).where( models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    found_vote = session.exec(statement).first()

    if vote.dir:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User {current_user.id} has already voted on post {vote.post_id}" )
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        return {"message": "Successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
        
        session.delete(found_vote)
        session.commit()
        return {"message": "Successfully deleted vote"}