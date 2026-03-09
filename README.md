# Task Manager — QA Automation Project

Full-stack web application with automated testing covering UI, API, and Database layers.

## Tech Stack

### Application
- **FastAPI** — REST API backend
- **PostgreSQL** — main database (tasks storage)
- **MongoDB** — logging database (audit trail)
- **SQLAlchemy** — ORM for PostgreSQL

### Testing
- **Python + pytest** — test framework
- **Playwright** — UI testing
- **requests** — API testing
- **psycopg2** — direct PostgreSQL testing
- **pymongo** — direct MongoDB testing

## Project Structure
```
task_manager/
├── app/
│   ├── main.py          # FastAPI app + UI
│   ├── models.py        # PostgreSQL models
│   ├── database.py      # DB connections
│   └── routers/
│       └── tasks.py     # API endpoints
├── tests/
│   ├── ui/              # Playwright UI tests
│   ├── api/             # API tests
│   └── db/              # Database tests
├── conftest.py
└── pytest.ini
```

## How to Run

### 1. Install dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment
Create `.env` file:
```
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=task_manager
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=task_manager
```

### 3. Start the application
```bash
uvicorn app.main:app --reload
```

### 4. Run tests
```bash
# All tests
python -m pytest

# UI tests only
python -m pytest -m ui

# API tests only
python -m pytest -m api

# DB tests only
python -m pytest -m db

# With HTML report
python -m pytest --html=report.html --self-contained-html
```

## API Documentation
After starting the app, visit: `http://127.0.0.1:8000/docs`

## Test Coverage
- **UI**: Task creation, completion, deletion via browser
- **API**: GET, POST, PUT, DELETE endpoints
- **PostgreSQL**: CRUD operations directly on DB
- **MongoDB**: Log creation and querying