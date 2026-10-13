from collections.abc import Iterator
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.db import create_tables # 导入建表函数

@pytest.fixture
def database_path(tmp_path: Path) -> Path:
    return tmp_path / "test-cars.db"

@pytest.fixture
def client(database_path: Path) -> Iterator[TestClient]:
    app = create_app(database_path)
    # 直接手动执行建表，绕过lifespan问题！
    create_tables(database_path)
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def car_payload() -> dict:
    return {"make": "Toyota", "model": "Corolla", "year": 2024, "color": "Silver"}
