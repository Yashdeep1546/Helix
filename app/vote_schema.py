from sqlmodel import  SQLModel

class Vote(SQLModel):
    post_id: int
    dir: bool=True