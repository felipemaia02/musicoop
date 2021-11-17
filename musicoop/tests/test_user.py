from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from musicoop.app import app

client = TestClient(app)

def test_register_user():
    response = client.post("/user", json={"email": "email@email.com", "username": "usernametest", "name": "nametest", "password": "senha123"})

    assert response.status_code == 200
    assert response.json() == {"email": "email@email.com","username": "usernametest","name": "nametest"}

def test_login_token():
    response = client.post(
        "/login", 
        data={"username": "email@email.com", "password": "senha123"}
    )
    
    assert response.status_code == 200
