import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    # Set profile with microfone permission (unpack it from 4uxxq5yw.microphone.7z):
    profile = webdriver.FirefoxProfile()
    profile.profile_dir = "C:/GitHub/selenium-training/selenium/python-example/4uxxq5yw.microphone"
    # BUG: works only with /, but not with \\
    # BUG: FF remove original profile after exit!!! Unpack it before test in temporary folder?
    # TODO: how to minimize profile? Only permissions.sqlite is relevant

    # exact place for 32bit version only:
    # wd = webdriver.Firefox(firefox_binary='c:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')

    wd = webdriver.Firefox(profile)
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    # Todo: microphone sharing notification
    # hangupButton appears to be disabled (OK) - test fails
    driver.get("https://webrtc.github.io/samples/src/content/peerconnection/audio/")
    time.sleep(5)
    driver.find_element_by_id('callButton').click()
    time.sleep(5)
    driver.find_element_by_id('hangupButton').click()
    time.sleep(5)