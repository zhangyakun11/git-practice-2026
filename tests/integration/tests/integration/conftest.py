import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client():
    db_path = Path("cars.db")
    app = create_app(db_path)
    with TestClient(app) as test_client:
        yield test_client
    if db_path.exists():
        db_path.unlink()
