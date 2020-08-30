import json
import re

import requests
import random
from config import cache_one_day, get_redis_conn, city_dict_key


class LianjiaCrawler:
    headers = {
        'User-Agent': '',
        'Referer': 'https://baidu.com/',
        'Cookie': 'lianjia_uuid=a38a3d7b-c24a-49e2-a989-3b1dd4e8d2e9; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221735fec534a1b3-0aaa15a63cd4b7-b7a1334-1327104-1735fec534b1e2%22%2C%22%24device_id%22%3A%221735fec534a1b3-0aaa15a63cd4b7-b7a1334-1327104-1735fec534b1e2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; UM_distinctid=1735fec582b209-09751d7719788e-b7a1334-144000-1735fec582c23e; _ga=GA1.2.1560903044.1595042192; _smt_uid=5f12bdaf.2e35b120; hw_client_uid=1feb4830-cdd6-11ea-8f96-cfd34ff8ad6c; select_city=310000; lianjia_ssid=cfb46433-b7e9-4957-b37a-cf4ea4204673; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiNThhMjdhMzczYWViZTY5MWY4Njg3N2U2MzFjYjM3NGNjMjI3MGIzNGU3ZjcxNWQyYTBhMDk5MmI0YWEyYjM0MzNjOTJkMjk4ZGNjMDJmZWEzYTIwZTYyMjYxZTllYTBjMWRkN2FiZjUxMTNjZGU5NGY2MjQ2NzNkNTVhM2NlODQ3ODRhMjdmMDc3MzBlODRkODczMDRlY2U2OTMwMzU0MWIwNDM5NGY5ZGQ1MWNjMTYwZWIzOWQyYzBhMGFmODlhM2QzYjhmZjU0MzgzYjE3ZDA4OTg4MjJhNjg5YTZlYmYxYmMwYWQyNTA1YWFkZmFlNWNmMmE4NmUyYjNjNDA0MTVlZmMyMmFmOWJiMjllOGMxNjE2NWUwOTNmYmE1ZTAyNDViMmFmYWY1MzdjNzNiZTE3MDkxMjRkNDcxODhkYzc4N2JmNDdjMTRjZjBhMDQ3MjU5NWQ3YzIxZmFlZjgwOFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJkODM4N2Q3MFwifSIsInIiOiJodHRwczovL20ubGlhbmppYS5jb20vIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=; _gid=GA1.2.886831603.1598744844; _gat=1; _gat_past=1; _gat_new=1; _gat_global=1; _gat_new_global=1; CNZZDATA1254525948=655132361-1595037594-%7C1598744467; CNZZDATA1253491255=2055849685-1595037563-%7C1598743170; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1598285394,1598744844; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1598744844',
    }
    useragents = [
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
        {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
        {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
        {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]
    get_all_city_url = 'https://m.lianjia.com/city/'
    city_url_pattern = 'https://m.lianjia.com/{}/'
    ershoufang_pattern = 'https://m.lianjia.com/{}/ershoufang/index/pg{}/'
    city_dict = {}

    def __init__(self):
        self.get_citys()

    def get_citys(self):
        redis_connection = get_redis_conn()
        if redis_connection.get(city_dict_key) and json.loads(redis_connection.get(city_dict_key)):
            city_dict = json.loads(redis_connection.get(city_dict_key))
            self.city_dict = city_dict
        response = self.request(self.get_all_city_url)
        citys = re.findall(re.compile(r'<a href="https://m.lianjia.com/(.+?)/">(.+?)</a>'),
                           response.text)
        for city in citys:
            self.city_dict[city[1]] = city[0]
        redis_connection.set(city_dict_key, json.dumps(
            self.city_dict), cache_one_day)

    def request(self, url):
        self.headers['User-Agent'] = self.useragents[random.randint(0, len(self.useragents) - 1)]['User-Agent']
        response = requests.get(url, headers=self.headers)
        return response
