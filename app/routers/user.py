from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter( # common prefix for all routes in this router
    prefix="/users",
    tags=['Users']
)

# Send user data to the server: email and hashed password
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut) # response_model is a built-in parameter specifying the output schema
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict()) # upack the user data (email, password) dictionary into user model class.
    # commit to and refresh the database
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    return new_user

# Get user by specified ID given the database
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), ):
    user = db.query(models.User).filter(models.User.id == id).first() # match id to database

    # raise not found if user not in database
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user # to the client