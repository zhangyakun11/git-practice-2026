import re
from playwright.sync_api import Page, expect
# =========课程给的示例E2E测试 保留==========
def test_user_creates_car_in_browser(page: Page, live_server):
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()
    expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible()
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
# =========自己写的E2E新测试：编辑车辆，刷新页面数据不丢失==========
def test_user_edits_car_and_change_survives_reload(page: Page, live_server):
    # 1.打开新建页面，创建 Honda Civic 2022
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make").fill("Honda")
    page.get_by_label("Model").fill("Civic")
    page.get_by_label("Year").fill("2022")
    page.get_by_role("button", name="Create car").click()
    # 2.点击Edit car链接
    page.get_by_role("link", name="Edit car").click()
    # 3.修改 model=Accord  year=2023
    page.get_by_label("Model").fill("Accord")
    page.get_by_label("Year").fill("2023")
    page.get_by_role("button", name="Save changes").click()
    # 4.断言详情页标题 Honda Accord
    expect(page.get_by_role("heading", name="Honda Accord")).to_be_visible()
    # 5.页面刷新，验证修改还在
    page.reload()
    expect(page.get_by_role("heading", name="Honda Accord")).to_be_visible()
    # 使用id精准定位model字段，唯一元素，不会多元素冲突
    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text('"2023"')
