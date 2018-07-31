import urllib.request
from bs4 import BeautifulSoup


class Fc2:
    def __init__(self):
        # main_url = 'http://adult.contents.fc2.com/article_search.php?id=421499'
        self.main_url = 'http://adult.contents.fc2.com/article_search.php?id='

    def get_info(self, product_number):

        url = self.main_url + product_number
        with urllib.request.urlopen(url) as response:
            html = response.read()
            html_soup = BeautifulSoup(html, "html.parser")
            block_text = html_soup.find('div', class_='main_info_block').text
            print(block_text)
