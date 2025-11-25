from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_remove_participant_success():
    # ensure starting state
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    assert email in activities[activity_name]["participants"]

    resp = client.delete(f"/activities/{activity_name}/participant", params={"email": email})
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Removed {email} from {activity_name}"

    # email should no longer be present
    assert email not in activities[activity_name]["participants"]


def test_remove_participant_missing():
    activity_name = "Chess Club"
    missing_email = "unknown@example.org"

    # ensure missing
    assert missing_email not in activities[activity_name]["participants"]

    resp = client.delete(f"/activities/{activity_name}/participant", params={"email": missing_email})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not found in activity"
