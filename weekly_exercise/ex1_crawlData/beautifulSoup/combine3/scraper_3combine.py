from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

# Danh sách URL và định danh nguồn
urls = {
    "hsx": "https://banggia.dnse.com.vn/hsx",
    "hnx": "https://banggia.dnse.com.vn/hnx",
    "upcom": "https://banggia.dnse.com.vn/upcom"
}

# Khởi tạo trình duyệt Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Danh sách chứa dữ liệu của tất cả nguồn
all_data = []

for key, url in urls.items():
    print(f"Đang cào dữ liệu từ {url} ...")
    driver.get(url)
    
    # Chờ đủ thời gian để trang tải xong (điều chỉnh nếu cần)
    time.sleep(5)
    
    # Lấy mã nguồn trang sau khi render
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    # Giả sử các hàng dữ liệu được chứa trong các phần tử có thuộc tính data-testid kết thúc bằng "-row"
    rows = soup.find_all("div", {"data-testid": lambda x: x and x.endswith("-row")})
    
    for row in rows:
        # Lấy tất cả các thẻ <div> con chứa dữ liệu (dùng recursive để bao quát tất cả các ô)
        cells = row.find_all("div", recursive=True)
        row_data = [cell.get_text(strip=True) for cell in cells if cell.get_text(strip=True) != '']
        # Bạn có thể thêm một cột chỉ định nguồn nếu cần
        row_data.insert(0, key.upper())
        all_data.append(row_data)

driver.quit()

if not all_data:
    print("Không có dữ liệu được cào.")
else:
    # Tìm số lượng ô tối đa trong các hàng
    max_len = max(len(row) for row in all_data)
    # Đảm bảo mỗi hàng có số ô bằng nhau (pad thêm chuỗi rỗng nếu thiếu)
    for row in all_data:
        if len(row) < max_len:
            row.extend([""] * (max_len - len(row)))
    
    # Tạo tên cột mặc định, ví dụ: 'Source', 'Col_1', 'Col_2', ...
    columns = ['Source'] + [f"Col_{i}" for i in range(1, max_len)]
    
    combined_df = pd.DataFrame(all_data, columns=columns)
    
    # Lưu DataFrame thành file CSV chung
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "stock_data_3combine.csv")
    combined_df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    
    print(f"Dữ liệu của tất cả các nguồn đã được lưu vào {csv_path}")
