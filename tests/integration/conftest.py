import pytest
import sqlite3
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import create_app

@pytest.fixture
def client(tmp_path: Path):
    test_db_file = tmp_path / "testcars.db"

    # 建表，并且不立刻关闭连接，上下文管理器保证写完再退出
    with sqlite3.connect(test_db_file) as conn:
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

    # 强制sync，Linux CI刷新磁盘，确保表已经持久化写入
    import os
    os.sync()

    app = create_app(database_path=test_db_file)
    with TestClient(app) as test_client:
        yield test_client
