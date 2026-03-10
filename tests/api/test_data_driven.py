import pytest
import json
import os
import requests

def load_test_data(filename):
    filepath = os.path.join(os.path.dirname(__file__), "../data", filename)
    with open(filepath, "r") as f:
        return json.load(f)
    
tasks_data = load_test_data("tasks.json")
invalid_tasks_data = load_test_data("invalid_tasks.json")

@pytest.mark.api
@pytest.mark.parametrize("task", tasks_data)
def test_create_task_from_file(api_url, task):
    responce = requests.post(f"{api_url}/tasks/", json={
        "title": task["title"],
        "description": task["description"]
    })
    data = responce.json()

    assert responce.status_code == 201
    assert data["title"] == task["title"]
    assert data["is_completed"] == task["expected_completed"]

    # Clean up
    requests.delete(f"{api_url}/tasks/{data['id']}")

@pytest.mark.api
@pytest.mark.parametrize("task", invalid_tasks_data)
def test_invalid_task_returns_error(api_url, task):
    responce = requests.post(f"{api_url}/tasks/", json={
        "title": task["title"],
        "description": task["description"]
    })
    
    assert responce.status_code == task["expected_status"]
