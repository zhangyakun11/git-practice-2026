import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client(tmp_path):
    # 每个测试独立的临时数据库文件，不会污染真实cars.db
    test_db = tmp_path / "test-cars.db"
    app = create_app(database_path=test_db)
    with TestClient(app) as test_client:
        yield test_client
