import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import create_app
from app.database import initialize


@pytest.fixture
def client():
    # 使用独立的测试数据库，不和其他环境冲突
    db_path = Path("test_cars.db")
    # 关键：提前初始化数据表，解决 no such table: cars
    initialize(db_path)
    app = create_app(db_path)
    with TestClient(app) as test_client:
        yield test_client
    # 测试跑完自动清理数据库文件
    if db_path.exists():
        db_path.unlink()
