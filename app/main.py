from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import auth, post, user, vote

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print("Database connected and tables verified.")
    yield

app = FastAPI(lifespan=lifespan)

# Register routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)