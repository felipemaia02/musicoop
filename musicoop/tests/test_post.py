from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from musicoop.app import app

client = TestClient(app)


def test_get_posts():
    login_response = client.post(
        "/login", 
        data={"username": "email@email.com", "password": "senha123"}
    )
    token = login_response.json()["access_token"]

    response = client.get("/posts", headers={"Authorization": "Bearer " + token})
    
    assert response.status_code == 202

    
