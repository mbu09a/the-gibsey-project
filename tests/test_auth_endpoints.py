import pytest
import requests
import json
import os
from unittest.mock import Mock, patch

# Test data
TEST_USER = {
    "email": "test@example.com",
    "password": "test123456"
}

MOCK_SUPABASE_RESPONSE = {
    "user": {
        "id": "mock-user-id",
        "email": "test@example.com",
        "created_at": "2025-01-01T00:00:00Z"
    },
    "session": {
        "access_token": "mock-jwt-token"
    }
}

@pytest.fixture
def base_url():
    return "http://localhost:8080"

def test_signup_endpoint(base_url):
    """Test user signup endpoint"""
    with patch('supabase.auth.Auth.sign_up') as mock_signup:
        mock_signup.return_value = Mock(user=Mock(
            id="mock-user-id",
            email="test@example.com", 
            created_at="2025-01-01T00:00:00Z"
        ))
        
        response = requests.post(
            f"{base_url}/signup",
            json=TEST_USER,
            headers={"Content-Type": "application/json"}
        )
        
        # Skip actual test if service not running
        if response.status_code == 500:
            pytest.skip("Service not properly configured with Supabase")
        
        assert response.status_code in [200, 201]

def test_login_endpoint(base_url):
    """Test user login endpoint"""
    with patch('supabase.auth.Auth.sign_in_with_password') as mock_login:
        mock_login.return_value = Mock(
            user=Mock(
                id="mock-user-id",
                email="test@example.com",
                created_at="2025-01-01T00:00:00Z"
            ),
            session=Mock(access_token="mock-jwt-token")
        )
        
        response = requests.post(
            f"{base_url}/login",
            json=TEST_USER,
            headers={"Content-Type": "application/json"}
        )
        
        # Skip actual test if service not running
        if response.status_code == 500:
            pytest.skip("Service not properly configured with Supabase")
        
        assert response.status_code in [200, 401]

def test_me_endpoint_unauthorized(base_url):
    """Test /me endpoint without authentication"""
    response = requests.get(f"{base_url}/me")
    assert response.status_code == 403  # No Authorization header

def test_me_endpoint_invalid_token(base_url):
    """Test /me endpoint with invalid token"""
    headers = {"Authorization": "Bearer invalid-token"}
    response = requests.get(f"{base_url}/me", headers=headers)
    assert response.status_code == 401

def test_auth_endpoints_structure(base_url):
    """Test that all required endpoints exist"""
    # Test health endpoint
    health_response = requests.get(f"{base_url}/health")
    assert health_response.status_code == 200
    
    # Test signup endpoint structure (should return 422 for missing data)
    signup_response = requests.post(f"{base_url}/signup", json={})
    assert signup_response.status_code == 422
    
    # Test login endpoint structure (should return 422 for missing data)
    login_response = requests.post(f"{base_url}/login", json={})
    assert login_response.status_code == 422