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
