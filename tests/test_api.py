import pytest
from app.api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 404  # No root endpoint

def test_ask_endpoint():
    response = client.get("/ask?q=What is GDPR?")
    assert response.status_code == 200
    assert "answer" in response.json()

# Add more tests as you build features