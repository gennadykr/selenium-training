import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Opera()
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    # Doesn't work at all for Opera 43, opera opens with "data:," in ULR field
    # driver https://github.com/operasoftware/operachromiumdriver/releases/tag/v0.2.2
    driver.get("https://webrtc.github.io/samples/src/content/peerconnection/audio/")
    time.sleep(5)
    driver.find_element_by_id('callButton').click()
    time.sleep(5)
    driver.find_element_by_id('hangupButton').click()
    time.sleep(5)