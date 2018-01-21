from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get("https://selfdrivingcars.mit.edu/deeptraffic/")
logs = driver.get_log('browser')
print(logs)
train_button = driver.find_element_by_id("trainButton")
print(train_button)
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
print(logs)
logs = driver.get_log('browser')
print(logs)
if(train_success):
    time.sleep(0.1)
    eval_button = driver.find_element_by_id("evalButton")
    print(eval_button)
    eval_button.click()
    eval_success = False
    try:
        element = WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.ID, "eval_button"))
        )
    finally:
        print("finished")
        train_success = True
