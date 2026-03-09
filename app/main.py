from fastapi import FastAPI
from app.database import engine, Base
from app.routers import tasks

# Створюємо таблиці в PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="Simple Task Manager for QA practice",
    version="1.0.0"
)

# Підключаємо роутер
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Task Manager API is running!"}

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Task Manager</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
            input, textarea { width: 100%; padding: 8px; margin: 5px 0; }
            button { padding: 10px 20px; background: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background: #45a049; }
            .task { border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 5px; }
            .completed { background: #f0fff0; text-decoration: line-through; }
            .delete-btn { background: #f44336; float: right; }
            .complete-btn { background: #2196F3; }
        </style>
    </head>
    <body>
        <h1>Task Manager</h1>

        <h2>Add New Task</h2>
        <input id="title" placeholder="Task title" />
        <textarea id="description" placeholder="Description (optional)"></textarea>
        <button onclick="createTask()">Add Task</button>

        <h2>Tasks</h2>
        <div id="tasks"></div>

        <script>
            const API = 'http://127.0.0.1:8000';

            async function loadTasks() {
                const response = await fetch(`${API}/tasks/`);
                const tasks = await response.json();
                const container = document.getElementById('tasks');
                container.innerHTML = '';
                tasks.forEach(task => {
                    container.innerHTML += `
                        <div class="task ${task.is_completed ? 'completed' : ''}">
                            <button class="delete-btn" onclick="deleteTask(${task.id})">Delete</button>
                            <button class="complete-btn" onclick="completeTask(${task.id})">✓</button>
                            <strong>${task.title}</strong>
                            <p>${task.description || ''}</p>
                        </div>`;
                });
            }

            async function createTask() {
                const title = document.getElementById('title').value;
                const description = document.getElementById('description').value;
                await fetch(`${API}/tasks/`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({title, description})
                });
                document.getElementById('title').value = '';
                document.getElementById('description').value = '';
                loadTasks();
            }

            async function deleteTask(id) {
                await fetch(`${API}/tasks/${id}`, {method: 'DELETE'});
                loadTasks();
            }

            async function completeTask(id) {
                await fetch(`${API}/tasks/${id}`, {
                    method: 'PUT',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({is_completed: true})
                });
                loadTasks();
            }

            loadTasks();
        </script>
    </body>
    </html>
    """