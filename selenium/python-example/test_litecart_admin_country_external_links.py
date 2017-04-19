import pytest
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
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
    # wd = webdriver.Chrome()
    # 2) Firefox:
    # wd = webdriver.Firefox()
    # 3) Edge:
    # -fixed: https://developer.microsoft.com/en-us/microsoft-edge/platform/issues/11640597/
    wd = webdriver.Edge()

    # print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

# see http://stackoverflow.com/questions/19377437/python-selenium-webdriver-writing-my-own-expected-condition
class there_is_window_other_than(object):
    def __init__(self, olds):
        self.olds = olds

    def __call__(self, driver):
        currents = driver.window_handles
        news = [item for item in currents if item not in self.olds]
        if len(news) > 0:
            return news[0]
        else:
            return False



# @pytest.mark.skipif(1 == 1, reason="second test development" )
def test_countries(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    wait = WebDriverWait(driver, 15)
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(.,'Add New Country')]")))[0].click()

    new_window_links = \
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#content form a[target=_blank]")))

    print(driver.title)
    main_window = driver.current_window_handle
    old_windows = driver.window_handles

    for x in range(0,len(new_window_links )):
        new_window_links[x].click()
        new_window = wait.until(there_is_window_other_than(old_windows))
        driver.switch_to_window(new_window)
        #time.sleep(2)
        print(driver.title)
        driver.close()
        driver.switch_to_window(main_window)


    time.sleep(5)