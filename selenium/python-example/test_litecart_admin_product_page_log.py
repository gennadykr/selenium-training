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


def introduce_error(drw):
    drw.execute_script("setTimeout(function() { throw \"lalala\"; }, 1000);")
    time.sleep(2)


def test_example(driver):
    # Log in to admin
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    wait = WebDriverWait(driver, 15)
    # Open Catalog
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
    product_links = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//form[@name='catalog_form']//a[./../..//input[contains(@name,'product')] and not(./i)]")))

    for x in range(0, len(product_links)):
        product_links[x].click()
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#tab-general")))
        #introduce_error(driver)
        browser_log = driver.get_log("browser")
        for l in browser_log:
            print(l)
        if (len(browser_log)):
            assert(False),'somthing in browser log'
        driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
        product_links = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//form[@name='catalog_form']//a[./../..//input[contains(@name,'product')] and not(./i)]")))

    time.sleep(3)