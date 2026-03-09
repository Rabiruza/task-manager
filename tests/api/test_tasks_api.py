import pytest
import requests

@pytest.mark.api
def test_get_all_tasks(api_url):
    response = requests.get(f"{api_url}/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.api
def test_create_task(api_url):
    task_data = {
        "title": "New Test Task",
        "description": "Test description"
    }

    response = requests.post(f"{api_url}/tasks/", json=task_data)
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["is_completed"] == False
    assert "id" in data
    assert "created_at" in data

    # Clean up
    requests.delete(f"{api_url}/tasks/{data['id']}")

@pytest.mark.api
def test_get_single_task(api_url, created_task):
    response = requests.get(f"{api_url}/tasks/{created_task['id']}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == created_task["id"]
    assert data["title"] == created_task["title"]

@pytest.mark.api
def test_update_task(api_url, created_task):
    response = requests.put(f"{api_url}/tasks/{created_task['id']}", json={
        "is_completed": True})
    data = response.json()

    assert response.status_code == 200
    assert data["is_completed"] == True

@pytest.mark.api
def test_delete_task(api_url, created_task):
    # Створюємо задачу
    task = requests.post(f"{api_url}/tasks/", json={
        "title": "Task to delete"
    }).json()

    # Видаляємо
    response = requests.delete(f"{api_url}/tasks/{task['id']}")
    assert response.status_code == 204

    # Перевіряємо що не існує
    get_response = requests.get(f"{api_url}/tasks/{task['id']}")
    assert get_response.status_code == 404

@pytest.mark.api
def test_get_nonexistent_task(api_url):
    response = requests.get(f"{api_url}/tasks/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"