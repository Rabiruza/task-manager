from playwright.sync_api import Page, expect

class TaskPage:
    def __init__(self, page: Page):
        self.page = page
        self.title_input = page.locator("#title")
        self.description_input = page.locator("#description")
        self.add_button = page.get_by_role("button", name="Add Task")
        self.tasks_container = page.locator("#tasks")

    def open(self):
        self.page.goto("http://127.0.0.1:8000/ui")

    def add_task(self, title: str, description: str = ""):
        self.title_input.fill(title)
        if description:
            self.description_input.fill(description)
        self.add_button.click()

    def get_tasks_count(self):
        return self.tasks_container.locator(".task").count()

    def complete_task(self, index: int = 0):
        self.tasks_container.locator(".complete-btn").nth(index).click()

    def delete_task(self, index: int = 0):
        self.tasks_container.locator(".delete-btn").nth(index).click()

    def is_task_completed(self, index: int = 0):
        task = self.tasks_container.locator(".task").nth(index)
        task.wait_for()
        classes = task.get_attribute("class")
        return "completed" in classes