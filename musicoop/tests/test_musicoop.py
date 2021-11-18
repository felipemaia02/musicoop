from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from musicoop.app import app


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Musicoop": "v0.1.0"}
