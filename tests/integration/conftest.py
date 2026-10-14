import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import create_app

@pytest.fixture
def client(tmp_path: Path):
    test_db_file = tmp_path / "testcars.db"
    app = create_app(database_path=test_db_file)

    # 【关键改动】直接用app内部的数据库连接去建表，共用同一个数据库连接
    from app.database import get_db
    with next(get_db()) as conn:
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

    with TestClient(app) as c:
        yield c
