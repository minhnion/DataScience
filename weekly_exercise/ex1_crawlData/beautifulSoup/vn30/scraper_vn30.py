from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

# Khởi tạo trình duyệt Chrome với webdriver_manager để tự động tải chromedriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://banggia.dnse.com.vn/vn30"
driver.get(url)

time.sleep(5)

# Lấy mã nguồn trang sau khi render xong
html = driver.page_source

driver.quit()

# Phân tích HTML bằng BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Ví dụ: Tìm tất cả các hàng dữ liệu <tr> theo class cụ thể
rows = soup.find_all("tr", class_="full border-divider-main all:border-divider-main hover:all:bg-rowTable-hover bg-odd")

data_list = []
for row in rows:
    cells = row.find_all("td")
    row_data = []
    for cell in cells:
        # Ưu tiên lấy text từ thẻ <div> nếu có
        div_tag = cell.find("div")
        if div_tag:
            text = div_tag.get_text(strip=True)
        else:
            text = cell.get_text(strip=True)
        row_data.append(text)
    data_list.append(row_data)

# Chuyển dữ liệu thành DataFrame và lưu vào CSV
df = pd.DataFrame(data_list)
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "stock_data.csv")
df.to_csv(csv_path, index=False, header=False, encoding="utf-8-sig")

print(f"Dữ liệu đã được lưu vào {csv_path}")