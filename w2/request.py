import requests
from bs4 import BeautifulSoup
from w1.sql import MySqlHelper
from urllib.parse import urljoin
url = "https://top.baidu.com/board?tab=realtime"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

baidu_table = MySqlHelper()
baidu_table.CREATE("title","url", "desc", "hot")

articles = soup.find_all("div", class_="c-single-text-ellipsis")
print(articles[0].find_parent("a").prettify())
items = soup.select('a[class*="title_"][href]')

for item in items:
    article = item.select_one(".c-single-text-ellipsis")

    if article is None:
        continue

    title = article.get_text(strip=True)
    article_url = urljoin(url, item["href"])

    container = item.find_parent("div")
    desc_tag = container.select_one('[class*="hot-desc_"]')
    hot_tag = container.select_one('[class*="hot-index_"]')

    desc = desc_tag.get_text(strip=True) if desc_tag else ""
    hot = hot_tag.get_text(strip=True) if hot_tag else ""

    baidu_table.INSERT(title, article_url, desc, hot)
baidu_table.SAVE("baidu_hot.json")

print(baidu_table.SELECT())