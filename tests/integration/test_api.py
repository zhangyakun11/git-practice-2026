"""Tier3 API integration test for cars-crud FastAPI app"""
from fastapi.testclient import TestClient


def test_homepage(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200


def test_create_car(client: TestClient):
    payload = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2024
    }
    resp = client.post("/api/cars", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["make"] == "Toyota"
    assert "id" in data


def test_get_one_car(client: TestClient):
    # 先创建一辆车
    create_payload = {
        "make": "Honda",
        "model": "Civic",
        "year": 2023
    }
    create_resp = client.post("/api/cars", json=create_payload)
    car_id = create_resp.json()["id"]

    # 查询这辆车
    get_resp = client.get(f"/api/cars/{car_id}")
    assert get_resp.status_code == 200
    car_data = get_resp.json()
    assert car_data["model"] == "Civic"


def test_list_all_cars(client: TestClient):
    # 创建测试车辆
    client.post("/api/cars", json={"make": "BMW", "model": "X5", "year": 2022})
    resp = client.get("/api/cars")
    assert resp.status_code == 200
    car_list = resp.json()
    assert isinstance(car_list, list)


def test_update_car(client: TestClient):
    # 创建车辆
    payload = {"make": "Audi", "model": "A4", "year": 2021}
    create_resp = client.post("/api/cars", json=payload)
    car_id = create_resp.json()["id"]

    # 更新
    update_payload = {"make": "Audi", "model": "A4", "year": 2025}
    update_resp = client.put(f"/api/cars/{car_id}", json=update_payload)
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["year"] == 2025


def test_delete_car(client: TestClient):
    # 创建车辆
    payload = {"make": "Ford", "model": "Focus", "year": 2020}
    create_resp = client.post("/api/cars", json=payload)
    car_id = create_resp.json()["id"]

    # 删除
    del_resp = client.delete(f"/api/cars/{car_id}")
    assert del_resp.status_code == 204

    # 确认已删除
    get_resp = client.get(f"/api/cars/{car_id}")
    assert get_resp.status_code == 404
