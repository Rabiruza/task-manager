import pytest
from app.models import Task

@pytest.mark.db
def test_create_task_in_db(db_session):
    task = Task(
        title="DB Test Task",
        description="Testing PostgreSQL directly"
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.id is not None
    assert task.title == "DB Test Task"
    assert task.is_completed == False
    assert task.created_at is not None

    # Cleanup
    db_session.delete(task)
    db_session.commit()

@pytest.mark.db
def test_read_task_from_db(db_session):
    # Створюємо
    task = Task(title="Read Test Task")
    db_session.add(task)
    db_session.commit()

    # Читаємо
    found = db_session.query(Task).filter(Task.id == task.id).first()

    assert found is not None
    assert found.title == "Read Test Task"

    # Cleanup
    db_session.delete(task)
    db_session.commit()

@pytest.mark.db
def test_update_task_in_db(db_session):
    task = Task(title="Update Test Task")
    db_session.add(task)
    db_session.commit()

    # Оновлюємо
    task.is_completed = True
    task.title = "Updated Title"
    db_session.commit()
    db_session.refresh(task)

    assert task.is_completed == True
    assert task.title == "Updated Title"

    # Cleanup
    db_session.delete(task)
    db_session.commit()

@pytest.mark.db
def test_delete_task_from_db(db_session):
    task = Task(title="Delete Test Task")
    db_session.add(task)
    db_session.commit()
    task_id = task.id

    # Видаляємо
    db_session.delete(task)
    db_session.commit()

    # Перевіряємо що не існує
    found = db_session.query(Task).filter(Task.id == task_id).first()
    assert found is None