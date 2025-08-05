
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

# SQLAlchemy models need to be created in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Connect to the router modules
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Basic test
@app.get("/")
def root():
    return {"message": "Hello World"}