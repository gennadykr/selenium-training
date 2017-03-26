from shutil import copyfile
import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    # Set profile with microfone permission (unpack it from 4uxxq5yw.microphone.7z):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    profile_directory = os.path.join(__location__,'4uxxq5yw.microphone')
    profile = webdriver.FirefoxProfile(profile_directory )

    # TODO: how to minimize profile? Only permissions.sqlite is relevant
    # Permission denied:
    # profile_permissions_sqlite = os.path.join(__location__,'permissions.sqlite')
    # profile = webdriver.FirefoxProfile()
    # print(profile.profile_dir)
    # copyfile( profile_permissions_sqlite, profile.profile_dir)

    # exact place for 32bit version only:
    # wd = webdriver.Firefox(firefox_binary='c:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')

    wd = webdriver.Firefox(profile)
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("https://webrtc.github.io/samples/src/content/peerconnection/audio/")
    time.sleep(5)
    driver.find_element_by_id('callButton').click()
    time.sleep(5)
    driver.find_element_by_id('hangupButton').click()
    time.sleep(5)