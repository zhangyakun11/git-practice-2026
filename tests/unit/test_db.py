"""Tier2: Database repository / sqlite tests."""
import pytest
from pathlib import Path
import sqlite3
from app.database import connect

TEST_DB_PATH = Path("test_cars.db")

@pytest.fixture
def db_conn():
    # 每次测试创建全新测试数据库
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
    # 创建表
    with connect(TEST_DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            color TEXT
        )
        """)
    # yield给测试使用
    with connect(TEST_DB_PATH) as c:
        yield c
    # 测试结束清理文件
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


def test_create_car(db_conn: sqlite3.Connection):
    cur = db_conn.execute(
        "INSERT INTO cars(make, model, year, color) VALUES (?, ?, ?, ?) RETURNING id",
        ("Honda", "Civic", 2022, "red")
    )
    row = cur.fetchone()
    car_id = row["id"]
    assert car_id is not None

    select_cur = db_conn.execute("SELECT * FROM cars WHERE id=?", (car_id,))
    car = select_cur.fetchone()
    assert car["make"] == "Honda"
    assert car["model"] == "Civic"
    assert car["year"] == 2022
    assert car["color"] == "red"


def test_get_car_by_id(db_conn: sqlite3.Connection):
    cur = db_conn.execute(
        "INSERT INTO cars(make, model, year) VALUES (?, ?, ?) RETURNING id",
        ("BMW", "X5", 2023)
    )
    car_id = cur.fetchone()["id"]

    select_cur = db_conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,))
    found = select_cur.fetchone()
    assert found["make"] == "BMW"

    # 查询不存在id返回None
    bad_cur = db_conn.execute("SELECT * FROM cars WHERE id = ?", (9999,))
    assert bad_cur.fetchone() is None


def test_list_all_cars(db_conn: sqlite3.Connection):
    db_conn.execute("INSERT INTO cars(make, model, year) VALUES (?, ?, ?)", ("Audi", "A4", 2020))
    db_conn.execute("INSERT INTO cars(make, model, year) VALUES (?, ?, ?)", ("Tesla", "Model3", 2024))
    rows = db_conn.execute("SELECT * FROM cars").fetchall()
    assert len(rows) >= 2


def test_update_car(db_conn: sqlite3.Connection):
    cur = db_conn.execute(
        "INSERT INTO cars(make, model, year) VALUES (?, ?, ?) RETURNING id",
        ("Ford", "Focus", 2021)
    )
    car_id = cur.fetchone()["id"]
    db_conn.execute("UPDATE cars SET color=? WHERE id=?", ("blue", car_id))

    updated_row = db_conn.execute("SELECT * FROM cars WHERE id=?", (car_id,)).fetchone()
    assert updated_row["color"] == "blue"

    # 更新不存在id，影响行数0
    cursor = db_conn.execute("UPDATE cars SET color=? WHERE id=?", ("black", 9999))
    assert cursor.rowcount == 0


def test_delete_car(db_conn: sqlite3.Connection):
    cur = db_conn.execute(
        "INSERT INTO cars(make, model, year) VALUES (?, ?, ?) RETURNING id",
        ("Nissan", "Altima", 2022)
    )
    car_id = cur.fetchone()["id"]
    db_conn.execute("DELETE FROM cars WHERE id=?", (car_id,))

    check = db_conn.execute("SELECT * FROM cars WHERE id=?", (car_id,)).fetchone()
    assert check is None
    # 删除不存在id不会报错
    db_conn.execute("DELETE FROM cars WHERE id=?", (9999,))

