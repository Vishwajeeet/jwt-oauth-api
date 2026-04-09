import pytest
from fastapi import status

def test_create_task(client, auth_headers):
    """Test creating a new task."""
    response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "New Task",
            "description": "Task description"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "New Task"
    assert data["description"] == "Task description"
    assert "id" in data
    assert "created_at" in data

def test_create_task_unauthorized(client):
    """Test creating task without authentication."""
    response = client.post(
        "/tasks",
        json={
            "title": "New Task",
            "description": "Task description"
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_list_user_tasks(client, auth_headers, test_task):
    """Test listing user's tasks."""
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Test Task"

def test_list_user_tasks_empty(client, auth_headers):
    """Test listing tasks for user with no tasks."""
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_get_task_owner(client, auth_headers, test_task):
    """Test getting a task as its owner."""
    response = client.get(f"/tasks/{test_task.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"

def test_get_task_not_found(client, auth_headers):
    """Test getting a non-existent task."""
    response = client.get(
        "/tasks/00000000-0000-0000-0000-000000000000",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_task(client, auth_headers, test_task):
    """Test updating a task."""
    response = client.put(
        f"/tasks/{test_task.id}",
        headers=auth_headers,
        json={
            "title": "Updated Task",
            "description": "Updated description"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated description"

def test_delete_task(client, auth_headers, test_task):
    """Test deleting a task."""
    response = client.delete(f"/tasks/{test_task.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_task_verify_deletion(client, auth_headers, test_task):
    """Test that deleted task cannot be retrieved."""
    client.delete(f"/tasks/{test_task.id}", headers=auth_headers)
    
    response = client.get(f"/tasks/{test_task.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
