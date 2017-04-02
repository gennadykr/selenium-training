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


# @pytest.mark.skipif(1 == 1, reason="second test development" )
def test_countries(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    # String comparing:
    #   http://stackoverflow.com/questions/4806911/string-comparison-technique-used-by-python
    #   https://docs.python.org/3/tutorial/datastructures.html#comparing-sequences-and-other-types
    #   https://www.programiz.com/python-programming/operators
    # Arrays
    #   http://www.i-programmer.info/programming/python/3942-arrays-in-python.html?start=1

    # 1) Check country and zones sorting for http://localhost/litecart/admin/?app=countries&doc=countries
    #   a) Iterate through rows and columns collecting country names and checking number of zones
    #   b) For countries with zones follow link, check table sorting there, navigate to original page

    # (a)
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    wait = WebDriverWait(driver, 15)
    rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[name=countries_form] tr.row")))
    number_of_rows = len(rows)
    print(number_of_rows)
    country_names = [0 for i in range(number_of_rows)]
    for x in range(0, number_of_rows):
        row = rows[x]
        columns = row.find_elements(By.CSS_SELECTOR, "td")
        country = columns[4]
        zones = columns[5]

        # check sorting for county names:
        country_names[x] = country.text
        print(country_names[x])
        if (x > 0):
            assert country_names[x - 1] < country_names[x]

        # (b)
        number_of_zones = int(zones.text)
        print(number_of_zones)
        if (number_of_zones > 0):
            country.find_element(By.CSS_SELECTOR, "a").click()
            zones_rows = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#table-zones tr:not(.header)")))
            # The last row is for adding new zone, it is not zone itself!
            number_of_zones_rows = len(zones_rows) - 1
            zone_names = [0 for i in range(number_of_zones_rows)]
            for y in range(0, number_of_zones_rows):
                zones_row = zones_rows[y]
                zone_cell = zones_row.find_elements(By.CSS_SELECTOR, "td")[2]
                zone_names[y] = zone_cell.text
                # zone_names[y] = zone_cell.find_element(By.CSS_SELECTOR , "input").get_attribute("value")
                print(zone_names[y])
                if (y > 0):
                    assert zone_names[y - 1] < zone_names[y]
            # Come back
            driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
            rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[name=countries_form] tr.row")))


def test_geo_zones(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    # 2) Check zones sorting for each country at the page http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones

    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    wait = WebDriverWait(driver, 15)
    rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[name=geo_zones_form] tr.row")))
    number_of_rows = len(rows)
    print(number_of_rows)
    country_names = [0 for i in range(number_of_rows)]
    for x in range(0, number_of_rows):
        row = rows[x]
        columns = row.find_elements(By.CSS_SELECTOR, "td")
        country = columns[2]
        print(country.text)
        country.find_element(By.CSS_SELECTOR, "a").click()
        zones_rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#table-zones tr:not(.header)")))
        number_of_zones_rows = len(zones_rows) - 1
        print(number_of_zones_rows)
        zone_names = [0 for i in range(number_of_zones_rows)]
        for y in range(0, number_of_zones_rows):
            zones_row = zones_rows[y]
            zone_cell = zones_row.find_elements(By.CSS_SELECTOR, "td")[2]
            zone_names[y] = zone_cell.find_element(By.CSS_SELECTOR, "option[selected=selected]").text
            print(zone_names[y])
            if (y > 0):
                assert zone_names[y - 1] < zone_names[y]
        # Come back
        driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
        rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[name=geo_zones_form] tr.row")))
