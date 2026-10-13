import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import create_app
from app.database import initialize


@pytest.fixture
def client():
    db_path = Path("cars.db")
    initialize(db_path)
    app = create_app(db_path)
    with TestClient(app) as test_client:
        yield test_client
    # 测试完成清理数据库
    if db_path.exists():
        db_path.unlink()
