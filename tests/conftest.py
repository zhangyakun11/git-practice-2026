from collections.abc import Iterator
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import create_app

@pytest.fixture
def database_path(tmp_path: Path) -> Path:
    return tmp_path / "test-cars.db"

@pytest.fixture
def client(database_path: Path) -> Iterator[TestClient]:
    app = create_app(database_path)
    # 手动触发lifespan事件，强制执行数据库表创建
    import contextlib
    with contextlib.asynccontextmanager(app.router.lifespan_context):
        with TestClient(app) as test_client:
            yield test_client

@pytest.fixture
def car_payload() -> dict:
    return {"make": "Toyota", "model": "Corolla", "year": 2024, "color": "Silver"}
