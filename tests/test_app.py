import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"], dict)

def test_signup_success():
    response = client.post("/activities/Drama Club/signup?email=testuser@mergington.edu")
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Drama Club" in response.json()["message"]
    # Check participant added
    get_resp = client.get("/activities")
    assert "testuser@mergington.edu" in get_resp.json()["Drama Club"]["participants"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Art Workshop/signup?email=dupuser@mergington.edu")
    # Duplicate signup
    response = client.post("/activities/Art Workshop/signup?email=dupuser@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Unknown/signup?email=nouser@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_signup_activity_full():
    # Fill up Math Olympiad
    for i in range(10):
        client.post(f"/activities/Math Olympiad/signup?email=full{i}@mergington.edu")
    response = client.post("/activities/Math Olympiad/signup?email=overflow@mergington.edu")
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]
