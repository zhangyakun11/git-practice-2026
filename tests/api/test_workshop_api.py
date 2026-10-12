
# =========课程示例 保留==========
def test_post_car_returns_201_and_json(client):
    payload = {
        "make": "Ford",
        "model": "Fiesta",
        "year": 2018,
        "color": "Black",
    }
    response = client.post("/api/cars", json=payload)
    assert response.status_code == 201
    car = response.json()
    assert car["id"] > 0
    assert car["make"] == "Ford"
    assert car["model"] == "Fiesta"
    assert response.headers["location"] == f"/api/cars/{car['id']}"


# =========自己写的新测试==========
def test_invalid_year_is_not_saved(client):
    bad_payload = {
        "make": "Toyota",
        "model": "Camry",
        "year": 1800,
        "color": "Grey"
    }
    # post提交非法年份
    resp_post = client.post("/api/cars", json=bad_payload)
    # 校验返回状态码422
    assert resp_post.status_code == 422

    # get获取全部车辆
    resp_get = client.get("/api/cars")
    car_list = resp_get.json()
    # 数据库不保存这条非法数据，列表为空
    assert car_list == []
