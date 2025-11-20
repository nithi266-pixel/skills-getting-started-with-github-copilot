from fastapi.testclient import TestClient
import pytest
import httpx
from app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)


def test_signup_and_unregister_flow():
    resp = client.get("/activities")
    assert resp.status_code == 200
    activities = resp.json()

    if not activities:
        pytest.skip("No activities available to test signup/unregister flow")

    activity_name = next(iter(activities.keys()))
    test_email = "test_student@example.com"

    # Sign up
    resp = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert resp.status_code == 200
    assert "message" in resp.json()

    # Verify participant added
    resp = client.get("/activities")
    participants = resp.json()[activity_name]["participants"]
    assert test_email in participants

    # Unregister
    resp = client.post(f"/activities/{activity_name}/unregister?email={test_email}")
    assert resp.status_code == 200
    assert "message" in resp.json()

    # Verify removed
    resp = client.get("/activities")
    participants = resp.json()[activity_name]["participants"]
    assert test_email not in participants