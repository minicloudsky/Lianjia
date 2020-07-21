import json
import re

import requests

from config import cache_one_day, get_redis_conn, city_dict_key


class LianjiaCrawler:
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/40.0 Mobile/12F69 Safari/600.1.4',
        'Referer': 'https://baidu.com/',
    }
    get_all_city_url = 'https://m.lianjia.com/city/'
    city_url_pattern = 'https://m.lianjia.com/{}/'
    ershoufang_pattern = 'https://m.lianjia.com/{}/ershoufang/index/pg{}/'
    city_dict = {}

    def __init__(self):
        self.get_citys()

    def get_citys(self):
        redis_connection = get_redis_conn()
        if redis_connection.get(city_dict_key):
            city_dict = json.loads(redis_connection.get(city_dict_key))
            self.city_dict = city_dict
        response = requests.get(self.get_all_city_url, headers=self.headers)
        citys = re.findall(re.compile(r'<a href="https://m.lianjia.com/(.+?)/">(.+?)</a>'),
                           response.text)
        for city in citys:
            self.city_dict[city[1]] = city[0]
        redis_connection.set(city_dict_key, json.dumps(self.city_dict), cache_one_day)
