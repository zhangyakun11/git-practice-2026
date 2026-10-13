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
        help="Show browser window when running E2E tests (not headless)"
    )


@pytest.fixture(scope="module")
def live_server(tmp_path: Path) -> Iterator[str]:
    # 自动获取空闲端口，避免端口占用冲突
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        host, port = sock.getsockname()

    config = uvicorn.Config(
        create_app(tmp_path / "browser-cars.db"),
        host=host,
        port=port,
        log_level="error",
        ws="none",
    )
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run)
    thread.start()

    # 等待服务启动
    for _ in range(20):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
            break
        except ConnectionRefusedError:
            time.sleep(0.2)

    yield f"http://{host}:{port}"
    server.should_exit = True
    thread.join()


@pytest.fixture
def playwright_context(playwright, request):
    show_browser = request.config.getoption("--show-browser")
    browser = playwright.chromium.launch(headless=not show_browser)
    context = browser.new_context()
    yield context
    context.close()
    browser.close()


@pytest.fixture
def page(playwright_context):
    return playwright_context.new_page()
