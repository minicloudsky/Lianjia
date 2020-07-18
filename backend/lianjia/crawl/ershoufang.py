from backend.lianjia.crawl.crawler import LianjiaCrawler
import requests
import re


class ErShouFang(LianjiaCrawler):
    total_page = 500

    def __init__(self):
        super().__init__()
        self.get_total_page(self.city_dict['上海'])

    def get_total_page(self, city_url):
        city_url = self.ershoufang_pattern.format(city_url, 1)
        print(city_url)
        response = requests.get(self.ershoufang_pattern.format(city_url, 1), headers=self.headers)
        try:
            page = re.findall(re.compile('{"hasQueryStr":true,"totalCount":(.+?),"returnCount"'), response.text)
            print(response.text)
            if isinstance(page, int):
                self.total_page = page
                print(self.total_page)
        except:
            pass


if __name__ == '__main__':
    ershoufang = ErShouFang()
