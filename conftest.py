import pytest
import requests
from playwright.sync_api import Page
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "http://127.0.0.1:8000"

# PostgreSQL сесія для тестів
@pytest.fixture
def db_session():
    POSTGRES_URL = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:"
        f"{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )
    engine = create_engine(POSTGRES_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

# MongoDB колекція для тестів
@pytest.fixture
def mongo_logs():
    client = MongoClient(
        host=os.getenv("MONGO_HOST"),
        port=int(os.getenv("MONGO_PORT"))
    )
    db = client[os.getenv("MONGO_DB")]
    yield db["logs"]
    client.close()

# Base URL для API тестів
@pytest.fixture
def api_url():
    return BASE_URL

# Створити задачу і видалити після тесту
@pytest.fixture
def created_task(api_url):
    response = requests.post(f"{api_url}/tasks/", json={
        "title": "Test Task",
        "description": "Created by fixture"
    })
    task = response.json()
    yield task
    requests.delete(f"{api_url}/tasks/{task['id']}")