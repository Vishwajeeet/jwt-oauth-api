import pytest
from fastapi import status
from unittest.mock import patch, AsyncMock

def test_google_callback_new_user(client, db):
    """Test Google OAuth callback with new user."""
    with patch('app.services.oauth_service.httpx.post') as mock_post, \
         patch('app.services.oauth_service.httpx.get') as mock_get:
        
        # Mock token response
        mock_post.return_value.json.return_value = {
            "access_token": "google_access_token",
            "token_type": "Bearer"
        }
        
        # Mock userinfo response
        mock_get.return_value.json.return_value = {
            "sub": "google_user_123",
            "email": "googleuser@example.com"
        }
        
        response = client.post(
            "/oauth/google/callback?code=auth_code_123"
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

def test_google_callback_existing_user(client, test_user, db):
    """Test Google OAuth callback with existing user."""
    with patch('app.services.oauth_service.httpx.post') as mock_post, \
         patch('app.services.oauth_service.httpx.get') as mock_get:
        
        # Mock token response
        mock_post.return_value.json.return_value = {
            "access_token": "google_access_token",
            "token_type": "Bearer"
        }
        
        # Mock userinfo response - same email as test user
        mock_get.return_value.json.return_value = {
            "sub": "google_user_456",
            "email": "test@example.com"
        }
        
        response = client.post(
            "/oauth/google/callback?code=auth_code_123"
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data

def test_github_callback_new_user(client, db):
    """Test GitHub OAuth callback with new user."""
    with patch('app.services.oauth_service.httpx.post') as mock_post, \
         patch('app.services.oauth_service.httpx.get') as mock_get:
        
        # Mock token response
        mock_post.return_value.json.return_value = {
            "access_token": "github_access_token",
            "token_type": "Bearer"
        }
        
        # Mock userinfo response
        mock_get.return_value.json.return_value = {
            "id": 12345,
            "login": "githubuser",
            "email": "githubuser@example.com"
        }
        
        response = client.post(
            "/oauth/github/callback?code=auth_code_456"
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

def test_github_callback_no_email_fallback(client, db):
    """Test GitHub OAuth callback without email (fallback to login)."""
    with patch('app.services.oauth_service.httpx.post') as mock_post, \
         patch('app.services.oauth_service.httpx.get') as mock_get:
        
        mock_post.return_value.json.return_value = {
            "access_token": "github_access_token"
        }
        
        mock_get.return_value.json.return_value = {
            "id": 67890,
            "login": "githubuser2"
        }
        
        response = client.post(
            "/oauth/github/callback?code=auth_code_789"
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
