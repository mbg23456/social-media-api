# Define fixtures in this file: these will automatically be available to all test files in the tests directory.


import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models
from alembic import command

# Reference a new database
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}'\
    f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Testing_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



#Base = declarative_base()


# def overrride_get_db():
#     db = Testing_SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# Swap any Depends(get_db) with the override function
#app.dependency_overrides[get_db] = overrride_get_db

client = TestClient(app)




# Insert fixture -- sqlalchemy

# Return client to use in tests
# Return database
@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Testing_SessionLocal()
    try:
        yield db # yield the database object itself
    finally:
        db.close()

@pytest.fixture#(scope="module")
def client(session):
    def overrride_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrride_get_db

    yield TestClient(app)

# Client runs after session. 


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "max2@gmail.com",
        "password": "password123"
    }
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']  # Add password to the new_user dict
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "max@gmail.com",
        "password": "password123"
    }
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']  # Add password to the new_user dict
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})

@pytest.fixture
def authorised_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    } # adding the token to the headers

    return client



@pytest.fixture
def test_posts(test_user, test_user2, session): # session for database access
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },
    {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts






'''
# Insert fixture -- alembic
@pytest.fixture
def client():
    command.upgrade(engine, "head") # Upgrade the database to the latest revision
    yield TestClient(app)
    # code to run after here ...
    command.downgrade(engine, "base")  # Downgrade the database to the base revision
'''