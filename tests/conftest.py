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
    # create_app内部 lifespan 会自动创建数据表
    app = create_app(database_path)
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def car_payload() -> dict:
    return {"make": "Toyota", "model": "Corolla", "year": 2024, "color": "Silver"}
