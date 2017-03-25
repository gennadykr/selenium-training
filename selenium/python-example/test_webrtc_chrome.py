import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    # Using of command line switch to enable microphone
    # Note that Crome has many helpfull command line switches for WebRTC testing!

    # Variant 1:
    # wd = webdriver.Chrome(desired_capabilities={"chromeOptions":{"args":["--use-fake-ui-for-media-stream"]}})

    # Variant 2:
    options = webdriver.ChromeOptions()
    #options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    options.add_argument("use-fake-ui-for-media-stream")
    wd = webdriver.Chrome(chrome_options=options)
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def test_example(driver):
    # Todo: better chekcs
    driver.get("https://webrtc.github.io/samples/src/content/peerconnection/audio/")
    driver.find_element_by_id('callButton').click()
    time.sleep(10)
    driver.find_element_by_id('hangupButton').click()
    time.sleep(5)