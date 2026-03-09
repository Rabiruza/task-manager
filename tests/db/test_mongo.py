import pytest
from datetime import datetime

@pytest.mark.db
def test_log_created(mongo_logs):
    # Вставляємо лог
    log = {
        "action": "create",
        "task_id": 999,
        "title": "Test Log",
        "timestamp": datetime.now()
    }
    result = mongo_logs.insert_one(log)

    assert result.inserted_id is not None

    # Cleanup
    mongo_logs.delete_one({"_id": result.inserted_id})

@pytest.mark.db
def test_find_log_by_action(mongo_logs):
    # Вставляємо кілька логів
    mongo_logs.insert_many([
        {"action": "create", "task_id": 1, "timestamp": datetime.now()},
        {"action": "update", "task_id": 1, "timestamp": datetime.now()},
        {"action": "delete", "task_id": 1, "timestamp": datetime.now()},
    ])

    # Знаходимо тільки create логи
    create_logs = list(mongo_logs.find({"action": "create"}))
    assert len(create_logs) > 0
    assert all(log["action"] == "create" for log in create_logs)

    # Cleanup
    mongo_logs.delete_many({"task_id": 1})

@pytest.mark.db
def test_count_logs_for_task(mongo_logs):
    task_id = 888
    # Вставляємо 3 логи для однієї задачі
    mongo_logs.insert_many([
        {"action": "create", "task_id": task_id, "timestamp": datetime.now()},
        {"action": "update", "task_id": task_id, "timestamp": datetime.now()},
        {"action": "delete", "task_id": task_id, "timestamp": datetime.now()},
    ])

    count = mongo_logs.count_documents({"task_id": task_id})
    assert count == 3

    # Cleanup
    mongo_logs.delete_many({"task_id": task_id})