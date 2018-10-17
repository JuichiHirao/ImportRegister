from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.request
import os
from bs4 import BeautifulSoup
from javcore import data
from javcore import db


class PackageImage:

    def __init__(self):

        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options, executable_path='c:\\SHARE\\chromedriver.exe')
        self.main_url = 'http://javarchive.com/'
        # self.main_url = 'http://javarchive.com/category/av-censored/'
        self.store_path = "D:\DATA\jav-save"

        self.jav_dao = db.jav.JavDao()
        self.jav2_dao = db.jav2.Jav2Dao()

    def get_url(self, id):

        jav = data.JavData()

        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        javs = self.jav_dao.get_where_agreement('WHERE id = ' + str(id))

        if javs is None:
            print('id [' + str(id) + '] not found.')
            return

        jav = javs[0]
        if len(jav.productNumber) <= 0:
            print('p_number is None')
            return

        print('  p_number [' + jav.productNumber + ']')
        edit_p = '%' + jav.productNumber + '%'
        jav2s = self.jav2_dao.get_where_agreement_param('WHERE title like %s', (edit_p, ))

        for jav2 in jav2s:

            print(jav2.title + ' ' + jav2.url)

            with urllib.request.urlopen(jav2.url) as response:
                content_html = response.read()
                content_html_soup = BeautifulSoup(content_html, "html.parser")
                post_content = content_html_soup.find('div', class_="post-meta-single")
                content_links = post_content.find_all('img')
                for content in content_links:
                    package_url = content.attrs['src']
                    filename = package_url[package_url.rfind("/") + 1:]
                    pathname = os.path.join(self.store_path, filename)
                    print('  package_url [' + package_url + ']')
                    result = urllib.request.urlretrieve(package_url, pathname)
                    print(str(result))
                    self.jav_dao.update_package(id, filename)
                    break


if __name__ == '__main__':
    p_image = PackageImage()
    # jav2.get_url('tat_035')
    p_image.get_url(5511)
