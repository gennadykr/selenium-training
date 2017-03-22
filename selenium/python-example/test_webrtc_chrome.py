import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    # Todo: microphone sharing notification
    # Todo: better checs, test passes successfull now while feature doesn't work (!!!)
    driver.get("https://webrtc.github.io/samples/src/content/peerconnection/audio/")
    driver.find_element_by_id('callButton').click()
    time.sleep(5)
    driver.find_element_by_id('hangupButton').click()
    time.sleep(5)