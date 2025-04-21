from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL (fallback to SQLite for MVP)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./api_monitor.db")

# Create engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Initialize database (create tables)
def init_db():
    SQLModel.metadata.create_all(engine)

# Dependency for FastAPI routes
def get_session():
    with Session(engine) as session:
        yield session
