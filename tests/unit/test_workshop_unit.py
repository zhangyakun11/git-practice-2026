from app.schemas import CarInput
import pytest
from pydantic import ValidationError


# ==========课程给的示例测试 保留==========
def test_car_text_fields_are_trimmed():
    car = CarInput(
        make=" Mazda ",
        model=" MX-5 ",
        year=2020,
        color=" Red "
    )
    assert car.make == "Mazda"
    assert car.model == "MX-5"
    assert car.color == "Red"


# =========自己写的新测试==========
def test_blank_model_is_rejected():
    # model是全空格，应当校验失败抛出ValidationError
    with pytest.raises(ValidationError):
        CarInput(make="Mazda", model=" ", year=2020)
