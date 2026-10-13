"""A real server and a fresh browser context for every E2E test."""
import os
import socket
import threading
import time
from collections.abc import Iterator
from pathlib import Path

import pytest
import uvicorn

from app.main import create_app


def pytest_addoption(parser):
    parser.addoption(
        "--show-browser",
        action="store_true",
        default=False,
        help="Run playwright tests with browser window visible (not headless)"
    )


@pytest.fixture(scope="function")
def live_server(tmp_path: Path) -> Iterator[str]:
    # Reserve a free port instead of hard-coding 8000 or racing another process.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        host, port = sock.getsockname()

        db_path = tmp_path / "browser-cars.db"
        app = create_app(db_path)

        config = uvicorn.Config(
            app,
            host=host,
            port=port,
            log_level="error",
            ws="none",
        )
        server = uvicorn.Server(config)

        # Start server in background thread
        thread = threading.Thread(target=server.run)
        thread.daemon = True
        thread.start()

        base_url = f"http://{host}:{port}"
        # Wait for server to be ready
        for _ in range(10):
            try:
                import requests
                requests.get(base_url, timeout=1)
                break
            except Exception:
                time.sleep(0.3)

        yield base_url

        # Shutdown server
        server.should_exit = True
        thread.join(timeout=2)


@pytest.fixture(scope="function")
def playwright_context(playwright, request, live_server):
    headed = request.config.getoption("--show-browser")
    browser = playwright.chromium.launch(headless=not headed)
    context = browser.new_context(base_url=live_server)
    yield context
    context.close()
    browser.close()


@pytest.fixture(scope="function")
def page(playwright_context):
    page = playwright_context.new_page()
    yield page
    page.close()
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app import database

@pytest.fixture(scope="function")
def client(tmp_path: Path):
    # 为集成测试创建临时db文件
    db_file = tmp_path / "test_cars.db"
    # 初始化数据库，执行建表语句
    database.init_db(db_file)
    app = create_app(db_file)
    yield TestClient(app)
