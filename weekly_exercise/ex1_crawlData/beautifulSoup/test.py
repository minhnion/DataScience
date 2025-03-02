import requests
from bs4 import BeautifulSoup

# URL của trang web muốn cào dữ liệu
url = "https://vnexpress.net"

# Gửi yêu cầu GET để lấy nội dung trang web
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)

# Kiểm tra xem request có thành công không
if response.status_code == 200:
    # Dùng BeautifulSoup để phân tích HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Lấy danh sách các tiêu đề bài viết
    articles = soup.find_all("h3", class_="title-news")  # Tùy thuộc vào trang web

    for index, article in enumerate(articles, start=1):
        title = article.text.strip()  # Lấy nội dung tiêu đề
        link = article.a["href"]  # Lấy link bài viết
        print(f"{index}. {title} - {link}")
else:
    print("Lỗi khi truy cập trang web:", response.status_code)
