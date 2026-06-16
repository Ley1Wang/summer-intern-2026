import requests
from bs4 import BeautifulSoup
from w1.sql import MySqlHelper
url = "https://top.baidu.com/board"

headers = {
    "User-Agent":
    "LeyiPhysicsBot/1.0 (leyiwang0624@gmail.com)"
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(
    response.text,
    "html.parser"
)


article = soup.find(
    "div",
    class_="c-single-text-ellipsis"
)
if article:
    print(article.get_text(strip=True))
else:
    print("没有找到目标内容")

baidu_table = MySqlHelper()
baidu_table.CREATE()