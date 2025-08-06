
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth, vote

# SQLAlchemy models need to be created in the database
# Not necessary if using Alembic for migrations
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pre-request CORS setup
# Determines which origins (sites) are allowed to make requests to the API
origins = ['https://www.google.com', 'https://www.facebook.com']
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connect to the router modules
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Basic test
@app.get("/")
def root():
    return {"message": "Hello World, introducing a minor change to Docker!"}