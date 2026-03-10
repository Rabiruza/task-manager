import pytest
from playwright.sync_api import Page, expect
from tests.ui.pages.task_page import TaskPage

@pytest.fixture
def task_page(page: Page):
    return TaskPage(page)

@pytest.mark.ui
def test_page_loads(task_page: TaskPage):
    task_page.open()
    expect(task_page.page).to_have_title("Task Manager")
    expect(task_page.add_button).to_be_visible()

@pytest.mark.ui
def test_add_task(task_page: TaskPage):
    task_page.open()
    initial_count = task_page.get_tasks_count()
    task_page.add_task("UI Test Task", "Test description")
    task_page.page.wait_for_timeout(500)
    assert task_page.get_tasks_count() == initial_count + 1

@pytest.mark.ui
def test_complete_task(task_page: TaskPage):
    task_page.open()
    task_page.add_task("Task to complete")
    task_page.page.wait_for_timeout(1000)

    count = task_page.get_tasks_count()
    task_page.complete_task(count - 1)
    task_page.page.wait_for_timeout(1000)
    assert task_page.is_task_completed(count - 1) == True

@pytest.mark.ui
def test_delete_task(task_page: TaskPage):
    task_page.open()
    task_page.add_task("Task to delete")
    task_page.page.wait_for_timeout(500)
    count_before = task_page.get_tasks_count()
    task_page.delete_task(0)
    task_page.page.wait_for_timeout(500)
    assert task_page.get_tasks_count() == count_before - 1