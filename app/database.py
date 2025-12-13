import os
from sqlmodel import create_engine, SQLModel
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DATABASE_USER", "appuser")
DB_PASS = os.getenv("DATABASE_PASSWORD", "changeme")
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = os.getenv("DATABASE_PORT", "3306")
DB_NAME = os.getenv("DATABASE_NAME", "salesdb")

DATABASE_URL = os.getenv("DATABASE_URL", f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# If using sqlite for quick local tests, DATABASE_URL can be sqlite:///./test.db
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True, pool_size=10, max_overflow=20)

def init_db():
    SQLModel.metadata.create_all(engine)
