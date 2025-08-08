
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.database import Base

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

'''
# Insert fixture -- alembic
@pytest.fixture
def client():
    command.upgrade(engine, "head") # Upgrade the database to the latest revision
    yield TestClient(app)
    # code to run after here ...
    command.downgrade(engine, "base")  # Downgrade the database to the base revision
'''