import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client(tmp_path):
    test_db_file = tmp_path / "testcars.db"
    app = create_app(database_path=test_db_file)
    with TestClient(app) as c:
        yield c
