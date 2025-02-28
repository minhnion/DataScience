from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


driver = webdriver.Chrome()

url = "https://finance.vietstock.vn/ket-qua-giao-dich"
driver.get(url)

time.sleep(5)
wait = WebDriverWait(driver, 10)

data = []
while True:
    table = driver.find_element(By.XPATH, '//*[@id="statistic-price"]')
    #table = driver.find_element(By.ID, "statistic-price")

    rows = table.find_elements(By.TAG_NAME,"tr")


    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        cols = [col.text.strip() for col in cols]
        if cols:
            data.append(cols)

    try:
        next_button = driver.find_element(By.XPATH,'//*[@id="btn-page-next"]')
        if "disable" in next_button.get_attribute("class"):
            print("Đã đến trang cuối")
            break
        next_button.click()
        print("Đang chuyển sang trang tiếp ...")
        time.sleep(5)
    except Exception as e:
        print("Không tìm thấy nút chuyển trang hoặc đến trang cuối")
        break

driver.quit()

df = pd.DataFrame(data)
print(df)

df.to_csv("table_data.csv", index=False, encoding="utf-8")