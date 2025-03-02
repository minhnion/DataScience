import requests
from bs4 import BeautifulSoup
import pandas as pd
import os  # Thêm thư viện os để lấy thư mục hiện tại

# URL của trang web cần cào
url = "https://banggia.dnse.com.vn/vn30"

# Gửi request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Tìm tất cả các hàng dữ liệu <tr>
    rows = soup.find_all("tr", class_="full border-divider-main all:border-divider-main hover:all:bg-rowTable-hover bg-odd")

    data_list = []
    
    for row in rows:
        cells = row.find_all("td")
        data = [cell.get_text(strip=True) for cell in cells]
        data_list.append(data)

    # Xác định đường dẫn của thư mục hiện tại
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Lấy thư mục chứa scraper.py
    csv_path = os.path.join(current_dir, "stock_data.csv")  # Đặt đường dẫn đến file CSV

    # Chuyển dữ liệu thành DataFrame và lưu vào CSV
    df = pd.DataFrame(data_list)
    df.to_csv(csv_path, index=False, header=False, encoding="utf-8-sig")

    print(f"Dữ liệu đã được lưu vào {csv_path}")
else:
    print("Lỗi khi truy cập trang web:", response.status_code)
