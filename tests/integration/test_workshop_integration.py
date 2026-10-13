from app import database
from app.schemas import CarInput

# =========课程示例 保留==========
def test_saved_car_can_be_read_from_sqlite(database_path):
    database.initialize(database_path)
    saved = database.create_car(
        database_path,
        CarInput(make="Toyota", model="Yaris", year=2020, color="Blue")
    )
    loaded = database.get_car(database_path, saved.id)

    assert loaded is not None
    assert loaded.id == saved.id
    assert loaded.make == "Toyota"
    assert loaded.year == 2020


# =========自己写的新测试==========
def test_deleting_one_car_keeps_the_other(database_path):
    # 初始化临时sqlite数据库
    database.initialize(database_path)

    # 创建两台车
    car1 = database.create_car(
        database_path,
        CarInput(make="Honda", model="Civic", year=2022, color="Black")
    )
    car2 = database.create_car(
        database_path,
        CarInput(make="Ford", model="Focus", year=2021, color="White")
    )

    # 删除第一台
    database.delete_car(database_path, car1.id)

    # 断言：car1已经查不到
    assert database.get_car(database_path, car1.id) is None
    # 断言：car2仍然存在
    assert database.get_car(database_path, car2.id) is not None

    car_list = database.list_cars(database_path)
    # 列表只能剩下car2，数量等于1
    assert len(car_list) == 1
    assert car_list[0].id == car2.id
