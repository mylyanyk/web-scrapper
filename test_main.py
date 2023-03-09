import os
from bs4 import BeautifulSoup
from main import WebScrapperTool

test_html = '<!DOCTYPE html> <html> <title>试题</title><body> <h1>测试头</h1> <p>测试段</p>' \
            ' <a href="https://fast.com/">测试链接</a> </body> </html>'

example_parsed_data = '<!DOCTYPE html> <html> <body> <h1>测试头</h1> <p>测试段</p> ' \
                      '<a href="https://fast.com/">测试链接</a> </body> </html>'


class TestWebScrapperTool:

    def test_parsed_data(self):
        scrapper = WebScrapperTool(page_html=test_html)
        assert scrapper.parsed_data == BeautifulSoup(example_parsed_data, 'html.parser')

    def test_get_headers(self):
        scrapper = WebScrapperTool(page_html=test_html)
        assert scrapper.get_headers() == ['测试头']

    def test_get_paragraphs(self):
        scrapper = WebScrapperTool(page_html=test_html)
        assert scrapper.get_paragraphs() == ['测试段']

    def test_get_links(self):
        scrapper = WebScrapperTool(page_html=test_html)
        assert scrapper.get_links() == ['https://fast.com/']

    def test_detect_language(self):
        scrapper = WebScrapperTool(page_html=test_html)
        assert scrapper.detect_language() == 'zh-cn'

    def test_write_to_csv(self):
        scrapper = WebScrapperTool(page_html=test_html)
        scrapper.write_to_csv('test_file.csv')

        assert os.path.isfile('test_file.csv')

    def test_write_to_db(self):
        scrapper = WebScrapperTool(page_html=test_html)

        scrapper.write_to_db('db_test.sqlite3')

        assert os.path.isfile('db_test.sqlite3')

