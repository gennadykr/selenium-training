import pytest
from selenium import webdriver
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
    wd = webdriver.Chrome()
    # 2) Firefox:
    # wd = webdriver.Firefox()
    # 3) Edge:
    # wd = webdriver.Edge()
    # print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def select_element_by_text(elements, pattern):
    assert len(elements)>0, "Empty list of elements"
    for x in range(0, len(elements)):
        if (pattern in elements[x].text):
            elements[x].click()
            return elements[x]
    raise("No element found with "+pattern)


def test_example(driver):
    # Log in to admin
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    # Open Catalog menu
    wait = WebDriverWait(driver, 15)
    menu_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#app- > a")))
    select_element_by_text(menu_items,'Catalog')
    #wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a/*[contains(.,'Catalog')]")))[0].click()

    # Click on "Add new Product" button
    add_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#content a.button")))
    select_element_by_text(add_buttons,'Product')
    #wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(.,'Add New Product')]")))[0].click()

    # Fill the form
    product_name = 'Chizhik-Pyzhik'
    product_code = 'ch001'
    product_image = \
        os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'chizhik_pyzhik_150x150.png'))
    print(product_image)

    tab_general = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#tab-general")))[0]
    tab_general.find_element(By.CSS_SELECTOR,"input[type=radio]").click()
    tab_general.find_element(By.CSS_SELECTOR,"input[name='name[en]']").send_keys(product_name)
    tab_general.find_element(By.CSS_SELECTOR,"input[name=code]").send_keys(product_code)
    quantity_field = tab_general.find_element(By.CSS_SELECTOR,"input[name=quantity]")
    quantity_field.clear()
    quantity_field.send_keys('3')

    sold_out_status = tab_general.find_element(By.CSS_SELECTOR,"select[name=sold_out_status_id]")
    selector = Select(sold_out_status)
    selector.select_by_visible_text('Temporary sold out')

    tab_general.find_element(By.CSS_SELECTOR,"input[name='new_images[]'").send_keys(product_image)

    # Switch on Information tab
    #select_element_by_text(driver.find_elements(By.CSS_SELECTOR,".tabs .index a"),'Information')
    driver.find_element(By.XPATH,"//a[contains(.,'Information')]").click()
    tab_information = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#tab-information")))[0]
    manufacturer_selector = tab_information.find_element(By.CSS_SELECTOR,"select[name=manufacturer_id]")
    selector = Select(manufacturer_selector)
    selector.select_by_visible_text('ACME Corp.')
    tab_information.find_element(By.CSS_SELECTOR,"[name='short_description[en]']").send_keys(product_name)
    tab_information.find_element(By.CSS_SELECTOR,".trumbowyg-editor").send_keys('Crystal crafts')

    # Switch on Information tab
    driver.find_element(By.XPATH,"//a[contains(.,'Prices')]").click()
    tab_prices = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#tab-prices")))[0]
    price_field=tab_prices.find_element(By.CSS_SELECTOR,"input[name=purchase_price]")
    price_field.clear()
    price_field.send_keys("3")
    tab_prices.find_element(By.CSS_SELECTOR,"input[name='prices[USD]']").send_keys("6")

    # Save
    driver.find_element(By.CSS_SELECTOR,"button[name=save]").click()

    # Check
    xpath_string = './/a[contains(.,\''+product_name+'\')]'
    print(xpath_string)
    catalog_form = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "form[name=catalog_form")))[0]
    catalog_form.find_element(By.XPATH,xpath_string).click()

    time.sleep(5)
