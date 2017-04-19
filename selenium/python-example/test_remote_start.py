import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
import os

@pytest.fixture
def driver(request):

    # 1) local grid:
    # 192.168.50.30:
    # java -jar selenium-server-standalone-2.53.1.jar -role hub
    # java -jar selenium-server-standalone-2.53.1.jar  -role node -browser browserName=chrome
    # 192.168.50.155:
    # java -jar selenium-server-standalone-2.53.1.jar  -role node -hub http://192.168.50.30:4444/wd/hub -browser "browserName=internet explorer"
    # see http://elementalselenium.com/tips/52-grid
    # I cannot use server 3.x, see https://github.com/SeleniumHQ/selenium/issues/3808

    #wd = webdriver.Remote("http://192.168.50.30:4444/wd/hub",desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)
    #wd = webdriver.Remote("http://192.168.50.30:4444/wd/hub",desired_capabilities=DesiredCapabilities.CHROME)

    # 2) browserstack
    # To change kay, use REST API, https://www.browserstack.com/automate/rest-api (Key)
    desired_cap = {'browser': 'chrome', 'build': 'First build', 'browserstack.debug': 'true' }
    #desired_cap = {'os': 'Windows', 'os_version': 'xp', 'browser': 'IE', 'browser_version': '7.0' }

    wd = webdriver.Remote(
        desired_capabilities=desired_cap)
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def test_local_grid(driver):
    driver.get("http://www.seleniumhq.org")
    time.sleep(5)
