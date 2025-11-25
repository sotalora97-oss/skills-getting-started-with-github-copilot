from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_signup_and_cleanup():
    activity = "Chess Club"
    email = "newstudent@example.org"

    # make sure the email isn't already in the list
    assert email not in activities[activity]["participants"]

    # sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Signed up {email} for {activity}"

    # verify it was added
    assert email in activities[activity]["participants"]

    # cleanup - remove the participant
    resp2 = client.delete(f"/activities/{activity}/participant", params={"email": email})
    assert resp2.status_code == 200
    assert email not in activities[activity]["participants"]
