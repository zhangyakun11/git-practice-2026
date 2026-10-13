from collections.abc import Iterator
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.database import Base, engine

@pytest.fixture
def database_path(tmp_path: Path) -> Path:
    return tmp_path / "test-cars.db"

@pytest.fixture
def client(database_path: Path) -> Iterator[TestClient]:
    # The context manager runs FastAPI's lifespan, including table creation.
    # Each test gets a fresh on-disk database, never the real cars.db.
    # 每次测试前，基于当前数据库路径，重建数据表
    app = create_app(database_path)
    # 执行生命周期事件，触发建表逻辑
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def car_payload() -> dict:
    return {"make": "Toyota", "model": "Corolla", "year": 2024, "color": "Silver"}

# 新增：自动创建数据表，适配CI环境，保证表一定存在
@pytest.fixture(autouse=True)
def setup_db_tables(database_path: Path):
    # 在每次测试运行前，创建全部数据表
    Base.metadata.create_all(bind=engine)
    yield
    # 测试结束后清理表
    Base.metadata.drop_all(bind=engine)
