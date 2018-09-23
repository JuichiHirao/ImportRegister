import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup


class Fc2:
    def __init__(self):
        self.main_url = 'http://adult.contents.fc2.com/article_search.php?id='
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]

        self.options = Options()
        self.options.add_argument('--headless')

    def __get_info_from_chrome(self, product_number):
        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path='c:\\SHARE\\chromedriver.exe')

        # print(self.main_url + product_number)
        self.driver.get(self.main_url + product_number)

        sleep(1)

        sell_date = ''
        seller = ''
        for main_info in self.driver.find_elements_by_css_selector('.main_info_block'):
            sleep(1)
            block_text = main_info.text
            # print(main_info.text)
            seller, sell_date = self.__parse_lines(block_text.splitlines())

        self.driver.close()

        return seller, sell_date

    def __parse_lines(self, lines):
        is_date = False
        is_seller = False
        for line in lines:
            if is_date:
                sell_date = line.strip()
                is_date = False
            if is_seller:
                seller = line.strip()
                is_seller = False

            if len(line.strip()) <= 0:
                continue
            if line.strip() == '販売日':
                is_date = True
            if line.strip() == '販売者':
                is_seller = True

        return seller, sell_date

    def __get_info(self, product_number):
        url = self.main_url + product_number
        sell_date = ''
        seller = ''
        urllib.request.install_opener(self.opener)
        with urllib.request.urlopen(url) as response:
            html = response.read()
            html_soup = BeautifulSoup(html, "html.parser")
            block_text = html_soup.find('div', class_='main_info_block').text
            # print(block_text)

            seller, sell_date = self.__parse_lines(block_text.splitlines())

        urllib.request.urlcleanup()

        return seller, sell_date

    def get_info(self, product_number):

        try:
            # sleep(3)
            # return self.__get_info(product_number)
            return self.__get_info_from_chrome(product_number)
        except:
            # return self.__get_info(product_number)
            return '', ''
            # return self.__get_info_from_chrome(product_number)

