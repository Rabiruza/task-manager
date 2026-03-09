from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# PostgreSQL
POSTGRES_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MongoDB
mongo_client = MongoClient(
    host=os.getenv("MONGO_HOST"),
    port=int(os.getenv("MONGO_PORT"))
)
mongo_db = mongo_client[os.getenv("MONGO_DB")]
logs_collection = mongo_db["logs"]