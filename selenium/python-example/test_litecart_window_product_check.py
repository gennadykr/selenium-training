import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color

@pytest.fixture
def driver(request):
    # 1) Chrome:
    # wd = webdriver.Chrome()

    # 2) Firefox:
    # wd = webdriver.Firefox()

    # 3) Edge:
    wd = webdriver.Edge()

    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def style_check(old_price_element,new_price_element):
    # How to check stroke and bold styles in any browser? I cannot find text-decoration for stroke in FF.
    # So I use "s"-tag for stroke and "strong"-tag for bold checks

    # check grey:
    old_price_color = old_price_element.value_of_css_property("color")
    print(old_price_color)
    old_price_color = Color.from_string(old_price_color)
    assert old_price_color.red == old_price_color.green
    assert old_price_color.green == old_price_color.blue

    # check red:
    new_price_color = new_price_element.value_of_css_property("color")
    print(new_price_color)
    new_price_color = Color.from_string(new_price_color)
    assert new_price_color.red > 0
    assert new_price_color.green == 0
    assert new_price_color.blue == 0

    # compare size, namely the height
    old_price_size = old_price_element.size
    print(old_price_size)
    new_price_size = new_price_element.size
    print(new_price_size)
    assert old_price_size['height'] < new_price_size['height']

def test_campaigns(driver):
    wait = WebDriverWait(driver, 15)
    driver.get("http://localhost/litecart/")
    product = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#box-campaigns li")))[0]
    link = product.find_element(By.CSS_SELECTOR,"a.link")
    name_element = product.find_element(By.CSS_SELECTOR,".name")
    regular_price_element = product.find_element(By.CSS_SELECTOR,"s.regular-price")
    campaign_price_element = product.find_element(By.CSS_SELECTOR,"strong.campaign-price")

    name = name_element.text
    print(name)
    regular_price = regular_price_element.text
    print(regular_price)
    campaign_price = campaign_price_element.text
    print(campaign_price)

    style_check(regular_price_element,campaign_price_element)

    # Go to the product page:
    link.click()
    product = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#box-product")))[0]
    name_element = product.find_element(By.CSS_SELECTOR,"[itemprop=name]")
    regular_price_element = product.find_element(By.CSS_SELECTOR,"s.regular-price")
    campaign_price_element = product.find_element(By.CSS_SELECTOR,"strong.campaign-price")

    assert name == name_element.text
    print(name)
    assert regular_price == regular_price_element.text
    print(regular_price)
    assert campaign_price == campaign_price_element.text
    print(campaign_price)

    style_check(regular_price_element,campaign_price_element)
