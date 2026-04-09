import pytest
from fastapi import status

def test_signup_success(client):
    """Test successful user signup."""
    response = client.post(
        "/auth/signup",
        json={"email": "newuser@example.com", "password": "Password123"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_signup_duplicate_email(client, test_user):
    """Test signup with duplicate email."""
    response = client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "Password123"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_signup_invalid_email(client):
    """Test signup with invalid email."""
    response = client.post(
        "/auth/signup",
        json={"email": "invalid-email", "password": "Password123"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_login_success(client, test_user):
    """Test successful login."""
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "TestPassword123"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_wrong_password(client, test_user):
    """Test login with wrong password."""
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "WrongPassword123"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_login_nonexistent_user(client):
    """Test login with nonexistent user."""
    response = client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "Password123"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_refresh_token_success(client, test_user):
    """Test successful token refresh."""
    login_response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "TestPassword123"}
    )
    refresh_token = login_response.json()["refresh_token"]
    
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data

def test_refresh_token_invalid(client):
    """Test token refresh with invalid token."""
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "invalid-token"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
