import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_signup_and_unregister():
    # Use a known activity and a test email
    activity = list(client.get("/activities").json().keys())[0]
    test_email = "testuser@mergington.edu"

    # Ensure not already signed up
    client.delete(f"/activities/{activity}/unregister?email={test_email}")

    # Sign up
    resp_signup = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp_signup.status_code == 200
    assert f"Signed up {test_email}" in resp_signup.json()["message"]

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp_dup.status_code == 400

    # Unregister
    resp_unreg = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert resp_unreg.status_code == 200
    assert f"Unregistered {test_email}" in resp_unreg.json()["message"]

    # Unregister again should fail
    resp_unreg2 = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert resp_unreg2.status_code == 400
