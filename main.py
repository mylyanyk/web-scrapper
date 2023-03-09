import time
import logging

import requests
import pandas as pd
from bs4 import BeautifulSoup
from langdetect import detect
import sqlite3


class WebScrapperTool:

    def __init__(self, url='', page_html=None):
        self.url = url
        self.page_html = page_html
        self.page_content = self._get_page_content()
        self.parsed_data = self._get_parsed_data()
        self.converted_to_df = self._convert_to_df()

    def _get_page_content(self) -> bytes:
        if self.url != '':
            page = requests.get(self.url)
            return page.content

    def _get_parsed_data(self) -> BeautifulSoup:
        if self.page_html is None:
            soup = BeautifulSoup(self.page_content, 'html.parser')
        else:
            soup = BeautifulSoup(self.page_html, 'html.parser')
        # removing unnecessary tags
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        return soup

    def get_all_visible_text(self) -> str:
        return self.parsed_data.get_text().replace('\n', '').strip()

    def get_headers(self) -> list:
        header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        all_headers = self.parsed_data.find_all(header_tags)
        return [header.text.replace('\n', '').strip() for header in all_headers]

    def get_paragraphs(self) -> list:
        paragraphs = self.parsed_data.find_all('p')
        return [paragraph.text.replace('\n', '').strip() for paragraph in paragraphs]

    def get_links(self) -> list:
        return [link.get('href') for link in self.parsed_data.find_all('a')]

    def detect_language(self) -> str:
        return detect(self.parsed_data.get_text())

    def _convert_to_df(self) -> pd.DataFrame:
        data = {'Header': self.get_headers(),
                'Paragraph': self.get_paragraphs(),
                'Link': self.get_links()}
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.transpose()
        df['URL'] = self.url
        df['Language'] = self.detect_language()
        return df

    def write_to_csv(self, csv_file='output.csv') -> None:
        self.converted_to_df.to_csv(csv_file, index=False)

    def write_to_db(self, db_file='db.sqlite3') -> None:
        conn = sqlite3.connect(db_file)
        self.converted_to_df.to_sql('website_data', conn, if_exists='replace', index=False)
        conn.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Starting URL scrapping...")
    URL = 'https://en.wikipedia.org/'
    scrapper = WebScrapperTool(URL)
    logging.info("Writing content to CSV and SQL files...")
    scrapper.write_to_db()
    scrapper.write_to_csv()
    # added sleep, so container doesn't exit after execution, and you could explore container files
    time.sleep(1000)

