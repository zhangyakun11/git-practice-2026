from collections.abc import Iterator
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from contextlib import asynccontextmanager
from app.main import create_app

@pytest.fixture
def database_path(tmp_path: Path) -> Path:
    return tmp_path / "test-cars.db"

@pytest.fixture
async def client(database_path: Path):
    app = create_app(database_path)
    # 正确执行FastAPI lifespan生命周期，触发建表
    async with app.router.lifespan_context(app):
        with TestClient(app) as test_client:
            yield test_client

@pytest.fixture
def car_payload() -> dict:
    return {"make": "Toyota", "model": "Corolla", "year": 2024, "color": "Silver"}
