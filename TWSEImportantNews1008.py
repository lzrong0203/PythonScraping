from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def getRealtimeNewsScreenShot(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://mops.twse.com.tw/mops/web/t05sr01_1")
    original_window = driver.current_window_handle
    button_list = driver.find_elements_by_xpath("//input[@value='詳細資料']")
    for i, button in enumerate(button_list):
        button.click()
        wait.until(EC.presence_of_element_located((By.ID, "table01")))
        driver.switch_to.window(driver.window_handles[1])
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tblHead")))
        entire = driver.find_element_by_tag_name("body")
        time.sleep(3)
        entire.screenshot(f"{i}.png")
        driver.close()
        driver.switch_to.window(original_window)
        if i > 2:
            break


options = Options()
options.headless = True
with webdriver.Firefox(executable_path="/Users/lzrong/Downloads/geckodriver",
                       options=options) as driver:
    getRealtimeNewsScreenShot(driver)
