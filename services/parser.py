import requests
from bs4 import BeautifulSoup
from utils import config
from datetime import datetime
from typing import List
import csv
import re
from api.schemas import NewsArticle
from services.news_service import save_articles

class Parser:
    def __init__(self, urls: List[str] = config.URLS):
        self.urls = urls
        self.news_articles = []
    def parse(self):
        for url in self.urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')

            for item in items:
                print(url)
                url_html = item.find('link').text
                content = None

                if url in [config.LENTA_URL, config.RIA_URL]:
                    content = self.parse_content(url, url_html)

                elif url in [config.RBC_URL]:
                    try:
                       content = item.find('rbc_news:full-text').text
                    except Exception:
                        content = None

                try:
                    category = item.find('category').text
                except Exception:
                    category = None

                na = NewsArticle(title = item.find('title').text,
                                 pub_date = datetime.strptime(item.find('pubDate').text, '%a, %d %b %Y %H:%M:%S %z'),
                                 category =category,
                                 link = item.find('link').text,
                                 resurse_name = config.RESURSE_NAMES[url],
                                 content = content)

                self.news_articles.append(na)

    def get_articles(self, to_csv=False):
        if to_csv:
            data_to_write = [article.dict() for article in self.news_articles]
            headers = data_to_write[0].keys()

            with open('news_articles.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()  # Write the header
                writer.writerows(data_to_write)

        return self.news_articles

    def parse_content(self,  url_rss: str, url_html: str):
        resource = requests.get(url_html)
        soup = BeautifulSoup(resource.text, 'html.parser')

        if url_rss == config.LENTA_URL:
            return soup.find('div', class_='topic-body__content').text

        elif url_rss == config.RIA_URL:
            text_blocks = soup.find('div', class_='article__body js-mediator-article mia-analytics').find_all('div', class_='article__text')
            return re.sub(r'^[^.]*[.]', '', ''.join([text_block.text for text_block in text_blocks])).strip()

    def save_articles_to_db(self):
        save_articles(self.get_articles())