from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get("https://selfdrivingcars.mit.edu/deeptraffic/")

train_button = driver.find_element_by_id("trainButton")
train_button.click()
train_success = False
try:
    element = WebDriverWait(driver, 1000).until(
        EC.element_to_be_clickable((By.ID, "trainButton"))
    )
finally:
    print("finished")
    #click OK button
    driver.find_element_by_class_name("confirm").click()
train_success = True

if(train_success):
    time.sleep(0.1)
    eval_button = driver.find_element_by_xpath('//*[@id="evalButton"]')
    eval_button.click()
    eval_success = False
    try:
        element = WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[7]/div/button"))
        )
    finally:
        print("finished")
        time.sleep(0.1)
        driver.save_screenshot('screenie.png')
        text_result = driver.find_element_by_xpath("/html/body/div[3]/p/b")
        print(text_result.get_attribute('innerHTML'))
