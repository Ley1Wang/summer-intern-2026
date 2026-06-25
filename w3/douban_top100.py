import re
import sqlite3

import requests
from bs4 import BeautifulSoup


class DoubanCrawler:
    def __init__(self):
        self.url = "https://movie.douban.com/top250"
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def crawl(self):
        movies = []

        for start in range(0, 100, 25):
            response = requests.get(
                self.url,
                params={"start": start},
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.select(".grid_view .item")

            for item in items:
                movies.append(self.parse_item(item))

        return movies[:100]

    def parse_item(self, item):
        rank = int(item.select_one(".pic em").text)
        title = item.select_one(".hd .title").text
        url = item.select_one(".hd a")["href"]
        rating = float(item.select_one(".rating_num").text)

        info = item.select_one(".bd p").get_text(" ", strip=True)
        year_match = re.search(r"\d{4}", info)
        year = int(year_match.group()) if year_match else None

        parts = [part.strip() for part in info.split("/") if part.strip()]
        category = parts[-1] if parts else ""

        comment_text = item.select_one(".star").get_text(" ", strip=True)
        comment_match = re.search(r"\d+", comment_text)
        comment_count = int(comment_match.group()) if comment_match else 0

        return {
            "rank": rank,
            "title": title,
            "year": year,
            "rating": rating,
            "comment_count": comment_count,
            "category": category,
            "url": url,
        }


class MovieDB:
    def __init__(self, db_name="douban_top100.db"):
        self.conn = sqlite3.connect(db_name)

    def create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS movies (
                rank INTEGER PRIMARY KEY,
                title TEXT,
                year INTEGER,
                rating REAL,
                comment_count INTEGER,
                category TEXT,
                url TEXT
            )
            """
        )

    def save(self, movies):
        sql = """
            INSERT OR REPLACE INTO movies
            (rank, title, year, rating, comment_count, category, url)
            VALUES
            (:rank, :title, :year, :rating, :comment_count, :category, :url)
        """
        self.conn.executemany(sql, movies)
        self.conn.commit()

    def close(self):
        self.conn.close()


def main():
    crawler = DoubanCrawler()
    movies = crawler.crawl()

    db = MovieDB()
    db.create_table()
    db.save(movies)
    db.close()

    print(f"Saved {len(movies)} movies.")


if __name__ == "__main__":
    main()
