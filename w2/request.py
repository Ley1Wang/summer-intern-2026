import requests
from bs4 import BeautifulSoup
from w1.sql import MySqlHelper
from urllib.parse import urljoin
url = "https://top.baidu.com/board"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

baidu_table = MySqlHelper()
baidu_table.CREATE("title","url", "desc", "hot")

articles = soup.find_all("div", class_="c-single-text-ellipsis")
print("articles数量:", len(articles))

for desc_tag,hot_tag, article in enumerate(articles, start=1):
    title = article.get_text(strip=True)
    desc = desc_tag.get_text(strip=True) if desc_tag else ""
    hot = hot_tag.get_text(strip=True) if hot_tag else ""
    link = article.find_parent("a")
    if link is None:
        link = article.find("a")

    if link and link.get("href"):
        article_url = urljoin(url, link["href"])
    else:
        article_url = ""
    if title:
        baidu_table.INSERT(title,article_url, "", "")

baidu_table.SAVE("baidu_hot.json")

print(baidu_table.SELECT())