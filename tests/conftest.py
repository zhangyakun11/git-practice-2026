# tests/conftest.py
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import create_app
from app import database

@pytest.fixture
def database_path(tmp_path: Path) -> Path:
    # 临时数据库文件
    return tmp_path / "cars.db"

@pytest.fixture(autouse=True)
def init_db_table(database_path: Path):
    # 初始化数据库+建表
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL,
        color TEXT
    )
    """)
    conn.commit()
    conn.close()

@pytest.fixture
def client(database_path: Path):
    # ✅ 重点：把临时数据库传给create_app！
    app = create_app(database_path)
    with TestClient(app) as test_client:
        yield test_client

