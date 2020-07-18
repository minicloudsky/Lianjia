import requests
import re
from backend.lianjia.config.config import redis_url, cache_one_day
import redis
import json


class LianjiaCrawler:
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/40.0 Mobile/12F69 Safari/600.1.4',
        'Referer': 'https://m.lianjia.com/',
        'Cookie': 'BIDUPSID=F571A6C7F45BFB8FFB9AA21F41A88AD9; PSTM=1591461785; BAIDUID=47ABB5FAB5BB5331FDB301890B9FA257:FG=1; ab_jid=78129331161d5d6ca9210c3b535741a9deea; ab_jid_BFESS=78129331161d5d6ca9210c3b535741a9deea; BDUSS=dsVHBMaDZKczc5djJNR2tGUHVDTVVoN2xUQ3IwVUxoREV1fllxdHFBTDVIRGRmSVFBQUFBJCQAAAAAAAAAAAEAAABuY2OBt-fWrtCh1MbM7AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPmPD1~5jw9fZH; MCITY=-%3A; H_PS_PSSID=1423_31671_31253_32045_32230_32117_31639; BDORZ=FFFB88E999055A3F8A630C64834BD6D0',
    }
    get_all_city_url = 'https://m.lianjia.com/city/'
    city_url_pattern = 'https://m.lianjia.com/{}/'
    ershoufang_pattern = 'https://m.lianjia.com/{}/ershoufang/index/pg{}/'
    newhouse_pattern = 'https://m.lianjia.com/{}/loupan/fang/'
    zufang_pattern = 'https://m.lianjia.com/chuzu/{}/zufang/'
    city_dict = {}

    def __init__(self):
        self.get_citys()

    def get_citys(self):
        city_dict_key = 'city_dict_v1'
        redis_connection = redis.Redis(host=redis_url)
        if redis_connection.get(city_dict_key):
            city_dict = json.loads(redis_connection.get(city_dict_key))
            self.city_dict = city_dict
        response = requests.get(self.get_all_city_url, headers=self.headers)
        citys = re.findall(re.compile(r'<a href="https://m.lianjia.com/(.+?)/">(.+?)</a>'),
                           response.text)
        for city in citys:
            self.city_dict[city[1]] = city[0]
        redis_connection.set(city_dict_key, json.dumps(self.city_dict), cache_one_day)


if __name__ == '__main__':
    crawler = LianjiaCrawler()
