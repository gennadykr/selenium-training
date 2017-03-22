import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    # 1) Chrome:
    wd = webdriver.Chrome()

    # 2) Firefox:
    # wd = webdriver.Firefox()

    # 3) Edge:
    # wd = webdriver.Edge()

    # 4) Firefox 45 ESR:
    # wd = webdriver.Firefox(capabilities={"marionette": False},
    #                       firefox_binary="c:\\Program Files (x86)\\Firefox45ESR\\firefox.exe")

    # 5) Fireox Nightly:
    # wd = webdriver.Firefox(capabilities={"marionette": True},
    #                       firefox_binary="c:\\Program Files (x86)\\Nightly\\firefox.exe")

    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    # WebDriverWait(driver, 10).until(EC.title_is("My Store"))
    time.sleep(5)
