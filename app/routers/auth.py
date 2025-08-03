# "Depends" from FastAPI allows us to use dependency injection
# This means we can declare in our code that we want to use a certain function or class
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# import modules from outside this folder
from .. import database, schemas, models, utils, oauth2

# for linkage to the main file
router = APIRouter(tags=['Authentication'])

# send data to the server 
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), # user credentials must have the OAuth2PasswordRequestForm type
                                                    # this is a class that FastAPI provides
                                                    # which must contain username and password (+ other optional fields)
           db: Session = Depends(database.get_db)): # A sql session with dependencies of database input parameter
                                                    # same as in the database.py file

    # check if the user exists
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    # if user does not exist, raise an error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    # if the password does not match, raise an error
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    # Otherwise ...

    # create a token
    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}