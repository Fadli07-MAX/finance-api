from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./items.db"
)

for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        print("Database connected successfully.")
        break
    except Exception as e:
        print(f"Database not ready ({i+1}/10): {e}")
        time.sleep(3)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()