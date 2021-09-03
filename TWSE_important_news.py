from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time

options = Options()
options.headless = False
realtime_news_url = "https://mops.twse.com.tw/mops/web/t05sr01_1"
day_news_url = "https://mops.twse.com.tw/mops/web/t05st02"


def get_daily_news_to_csv(driver, url):
    # driver = webdriver.Chrome(executable_path="/Users/lzrong/Downloads/chromedriver")
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    driver.find_element_by_id("year").clear()
    driver.find_element_by_id("year").send_keys("110")
    driver.find_element_by_id("month").send_keys("9")
    driver.find_element_by_id("day").send_keys("1")
    button = driver.find_element_by_xpath("//input[@value=' 查詢 ']")
    button.click()
    wait.until(EC.presence_of_element_located((By.ID, "fm")))
    forms = driver.find_elements_by_css_selector("form#fm table tbody tr")
    cols_name = []
    news_list = []
    for news in forms:
        # print(news.get_attribute("class"))
        if news.get_attribute("class") == "":
            for col in news.find_elements_by_class_name("tblHead"):
                cols_name.append(col.text)
            # print(cols_name)
        else:
            a_news = []
            for i in enumerate(news.find_elements_by_tag_name("td")):
                if i[0] == 5:
                    break
                else:
                    a_news.append(i[1].text)
                news_list.append(a_news)
        df = pd.DataFrame(news_list, columns=cols_name[:5])
        df.to_csv("news.csv")

def get_realtime_news_to_csv(driver, url):
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    original_window = driver.current_window_handle
    button_list = driver.find_elements_by_xpath("//input[@value='詳細資料']")
    for button in enumerate(button_list):
        button[1].click()
        wait.until(EC.presence_of_element_located((By.ID, "table01")))
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)
        driver.save_screenshot(f"{button[0]}.png")
        driver.close()
        driver.switch_to.window(original_window)


with webdriver.Firefox(executable_path="/Users/lzrong/Downloads/geckodriver",
                       options=options) as driver:
    # get_daily_news_to_csv(driver, day_news_url)
    get_realtime_news_to_csv(driver, realtime_news_url)
