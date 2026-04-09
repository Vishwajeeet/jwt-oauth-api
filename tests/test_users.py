import pytest
from fastapi import status

def test_get_current_user_profile(client, auth_headers):
    """Test getting current user profile."""
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "created_at" in data

def test_get_current_user_profile_unauthorized(client):
    """Test getting current user profile without authentication."""
    response = client.get("/users/me")
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_user_by_id_admin(client, admin_auth_headers, test_user):
    """Test getting user by ID as admin."""
    response = client.get(
        f"/users/{test_user.id}",
        headers=admin_auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "test@example.com"

def test_get_user_by_id_non_admin(client, auth_headers, test_user):
    """Test getting user by ID as non-admin."""
    response = client.get(
        f"/users/{test_user.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_update_current_user(client, auth_headers):
    """Test updating current user profile."""
    response = client.put(
        "/users/me",
        headers=auth_headers,
        json={"email": "newemail@example.com"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "newemail@example.com"

def test_update_current_user_password(client, auth_headers):
    """Test updating current user password."""
    response = client.put(
        "/users/me",
        headers=auth_headers,
        json={"password": "NewPassword123"}
    )
    assert response.status_code == status.HTTP_200_OK

def test_list_users_admin(client, admin_auth_headers, test_user):
    """Test listing all users as admin."""
    response = client.get("/users", headers=admin_auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # At least admin and test user

def test_list_users_non_admin(client, auth_headers):
    """Test listing all users as non-admin."""
    response = client.get("/users", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
