import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
import os

@pytest.fixture
def driver(request):
    # 1) Chrome:
    wd = webdriver.Chrome()
    # 2) Firefox:
    # wd = webdriver.Firefox()
    # 3) Edge:
    # wd = webdriver.Edge()
    # print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def test_cart(driver):
    wait = WebDriverWait(driver, 15)
    for x in range(0, 3):
        # Go to the 1st product page
        driver.get("http://localhost/litecart/")
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , ".product")))[0].click()

        # Add the product to the cart
        box_product = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#box-product")))[0]
        cart_item_quantity_element = driver.find_element(By.CSS_SELECTOR,"#cart-wrapper .quantity")
        cart_item_quantity = int(cart_item_quantity_element.text)
        print(cart_item_quantity)
        selectors = box_product.find_elements(By.CSS_SELECTOR , "select[name='options[Size]']")
        if (len(selectors) > 0):
            Select(selectors[0]).select_by_index(1)
        box_product.find_element(By.CSS_SELECTOR,"button[name=add_cart_product]").click()

        # Waiting new quantity counter in the cart
        while int(cart_item_quantity_element.text) <= cart_item_quantity:
            time.sleep(1)
        print(int(cart_item_quantity_element.text))

    time.sleep(10)
