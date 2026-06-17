import requests
from bs4 import BeautifulSoup
from w1.sql import MySqlHelper

url = "https://top.baidu.com/board"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
baidu_table = MySqlHelper()
baidu_table.CREATE("rank", "title", "desc", "hot")

articles = soup.find_all("div", class_="c-single-text-ellipsis")
print("articles数量:", len(articles))

for rank, article in enumerate(articles, start=1):
    title = article.get_text(strip=True)

    if title:
        baidu_table.INSERT(rank, title, "", "")

baidu_table.SAVE("baidu_hot.json")

print(baidu_table.SELECT())