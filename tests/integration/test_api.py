"""Tier3 API integration test for cars-crud FastAPI app"""
from fastapi.testclient import TestClient

async def test_homepage(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200

async def test_create_car(client: TestClient):
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

async def test_get_one_car(client: TestClient):
    payload = {"make":"Honda", "model":"CRV", "year":2023}
    res_create = client.post("/api/cars", json=payload)
    car_id = res_create.json()["id"]
    res_get = client.get(f"/api/cars/{car_id}")
    assert res_get.status_code == 200
    assert res_get.json()["model"] == "CRV"
    # 查询不存在车辆返回404
    res_404 = client.get("/api/cars/99999")
    assert res_404.status_code == 404

async def test_list_all_cars(client: TestClient):
    client.post("/api/cars", json={"make":"Kia", "model":"Sportage", "year":2022})
    resp = client.get("/api/cars")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

async def test_update_car(client: TestClient):
    res_create = client.post("/api/cars", json={"make":"Subaru", "model":"Impreza", "year":2021})
    car_id = res_create.json()["id"]
    # PUT使用完整CarInput
    res_update = client.put(
        f"/api/cars/{car_id}",
        json={"make":"Subaru", "model":"Impreza", "year":2021}
    )
    assert res_update.status_code == 200
    assert res_update.json()["model"] == "Impreza"

async def test_delete_car(client: TestClient):
    res_create = client.post("/api/cars", json={"make":"Mazda", "model":"CX5", "year":2020})
    car_id = res_create.json()["id"]
    res_del = client.delete(f"/api/cars/{car_id}")
    assert res_del.status_code == 204
    assert client.get(f"/api/cars/{car_id}").status_code == 404
