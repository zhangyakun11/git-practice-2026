import pytest
import sqlite3
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client(tmp_path):
    test_db_file: Path = tmp_path / "testcars.db"
    # 直接原生SQL建表，完全不依赖app/database.py里的initialize函数！
    conn = sqlite3.connect(test_db_file)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            color TEXT
        );
    """)
    conn.commit()
    conn.close()

    app = create_app(database_path=test_db_file)
    with TestClient(app) as c:
        yield c
