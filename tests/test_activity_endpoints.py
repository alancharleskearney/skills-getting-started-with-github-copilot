import urllib.parse


def test_get_activities_returns_data(client):
    # Arrange
    # (no setup needed beyond fixtures)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity_name)}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    refresh = client.get("/activities")
    participants = refresh.json()[activity_name]["participants"]
    assert email in participants


def test_signup_rejects_duplicate(client):
    # Arrange
    activity_name = "Chess Club"
    existing = "michael@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity_name)}/signup"

    # Act
    response = client.post(path, params={"email": existing})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_activity_not_found(client):
    # Arrange
    activity_name = "DoesNotExist"
    email = "test@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity_name)}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity_name)}/participants"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    refresh = client.get("/activities")
    participants = refresh.json()[activity_name]["participants"]
    assert email not in participants


def test_remove_nonexistent_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "notfound@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity_name)}/participants"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_remove_from_invalid_activity(client):
    # Arrange
    activity_name = "DoesNotExist"
    email = "anyone@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity_name)}/participants"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"