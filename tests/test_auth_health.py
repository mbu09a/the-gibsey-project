import pytest
import requests
import time
from docker import from_env
import os

def test_auth_backend_health():
    """Test that the auth backend health endpoint is accessible"""
    # Wait a moment for the service to start up
    time.sleep(2)
    
    try:
        response = requests.get("http://localhost:8080/health", timeout=10)
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
    except requests.exceptions.ConnectionError:
        pytest.fail("Auth backend service is not running or not accessible")
    except requests.exceptions.Timeout:
        pytest.fail("Auth backend service health check timed out")

def test_auth_backend_container_running():
    """Test that the auth backend container is running"""
    if os.getenv("SKIP_DOCKER_TESTS"):
        pytest.skip("Docker tests skipped")
    
    client = from_env()
    containers = client.containers.list()
    
    auth_container = None
    for container in containers:
        if "auth-backend" in container.name or "auth_backend" in container.name:
            auth_container = container
            break
    
    assert auth_container is not None, "Auth backend container not found"
    assert auth_container.status == "running", f"Auth backend container status: {auth_container.status}"