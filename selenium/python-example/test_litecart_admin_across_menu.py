import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    # 1) Chrome:
    wd = webdriver.Chrome()

    # 2) Firefox:
    # wd = webdriver.Firefox(firefox_binary='c:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')

    # 3) Edge:
    # wd = webdriver.Edge()

    # 4) Firefox 45 ESR:
    # wd = webdriver.Firefox(capabilities={"marionette": False},
    #                       firefox_binary="c:\\Program Files (x86)\\Firefox45ESR\\firefox.exe")

    # 5) Fireox Nightly:
    # wd = webdriver.Firefox(capabilities={"marionette": True},
    #                       firefox_binary="c:\\Program Files (x86)\\Nightly\\firefox.exe")

    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    # WebDriverWait(driver, 10).until(EC.title_is("My Store"))
    # time.sleep(5)
    # wait list1 > 0, click item, wait list2 > 0, click item
    # $$("#app- > a")
    # $$("#app-.selected li > a")
    # $$("#content > h1")
    wait = WebDriverWait(driver, 15)
    menu_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#app- > a")))
    number_of_items = len(menu_items)
    print(number_of_items)
    for x in range(0, number_of_items):
        menu_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#app- > a")))
        menu_items[x].click()
        header = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#content > h1")))
        print(header[0].text)
        submenu_items = driver.find_elements(By.CSS_SELECTOR , "#app-.selected li > a")
        number_of_subitems = len(submenu_items)
        print(number_of_subitems)
        if (number_of_subitems > 0):
            for y in range(0, number_of_subitems):
                submenu_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#app-.selected li > a")))
                submenu_items[y].click()
                headers = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#content > h1")))
                print(headers[0].text)

