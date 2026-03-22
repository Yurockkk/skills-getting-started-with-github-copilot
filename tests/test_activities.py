import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: No specific setup needed as activities are predefined in the app
    
    # Act: Make a GET request to the /activities endpoint
    response = client.get("/activities")
    
    # Assert: Check that the response is successful and contains expected data
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert len(data) == 9  # There are 9 activities

def test_signup_for_activity_success():
    # Arrange: Choose an activity and a new email not already signed up
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act: Make a POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert: Check successful signup
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    
    # Verify the participant was added
    get_response = client.get("/activities")
    activities = get_response.json()
    assert email in activities[activity_name]["participants"]

def test_signup_for_activity_already_signed_up():
    # Arrange: Use an email already signed up for the activity
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants
    
    # Act: Attempt to signup again
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert: Check that it fails with 400
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}

def test_signup_for_activity_not_found():
    # Arrange: Use a non-existent activity name
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"
    
    # Act: Try to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert: Check 404 response
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_unregister_from_activity_success():
    # Arrange: First signup a student, then unregister
    activity_name = "Programming Class"
    email = "teststudent@mergington.edu"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})  # Signup first
    
    # Act: Unregister the student
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert: Check successful unregistration
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    
    # Verify the participant was removed
    get_response = client.get("/activities")
    activities = get_response.json()
    assert email not in activities[activity_name]["participants"]

def test_unregister_from_activity_not_signed_up():
    # Arrange: Try to unregister a student not signed up
    activity_name = "Gym Class"
    email = "notsignedup@mergington.edu"
    
    # Act: Attempt to unregister
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert: Check 404 response
    assert response.status_code == 404
    assert response.json() == {"detail": "Student not signed up for this activity"}

def test_unregister_from_activity_not_found():
    # Arrange: Use a non-existent activity
    activity_name = "Fake Activity"
    email = "student@mergington.edu"
    
    # Act: Try to unregister
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert: Check 404 response
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}