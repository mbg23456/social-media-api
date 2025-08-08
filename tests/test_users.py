from app import schemas
from jose import jwt
import pytest
from app.config import settings


'''
def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.status_code == 200
    #assert res.json().get('message') == 'Hello World, introducing a minor change to Docker!'

'''

def test_create_user(client):
    res = client.post("/users/", json={"email": "person@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json()) # check it has the schema (class) properties
    assert new_user.email == "person@gmail.com"
    assert res.status_code == 201




def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']}) # has to be form data, not json
    login_res = schemas.Token(**res.json())  # check it has the schema (class) properties
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('max@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 400),
    ('max@gmail.com', None, 400)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"


















# add a decorator
'''
from app.calculations import add
@pytest.mark.parametrize("num1, num2, expected", [
    (2, 3, 5),
    (-5, -10, -15),
    (0, 0, 0),
    (100, 200, 300)
])
def testadd(num1, num2, expected):
    """Tests the add function."""
    # Asserting: if a true statment, nothing happens; if false, an AssertionError is raised.

    print("testing add function")

    assert add(num1, num2) == expected

'''