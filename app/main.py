from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
#After switching to SQLAlchemy ORM
#Schema / API validation  
#utls: auth
from . import models
from .database import engine
#routrs
from .routers import post, user, auth, vote
#enviroment variables
from .config import settings

#running db
#models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello"}