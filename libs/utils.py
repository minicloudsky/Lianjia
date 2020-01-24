import redis
import requests
from bs4 import BeautifulSoup
from spider.config import *
import json


def get_city():
    redis = get_redis()
    if redis.get('citys'):
        return json.loads(redis.get('citys'))
    url = 'https://m.lianjia.com/city/'
    response = requests.get(url, headers=header())
    soup = BeautifulSoup(response.text, 'html.parser')
    city_url = soup.find_all(attrs={"class": 'block city_block'})
    citys = []
    urls = []
    for c in city_url:
        for u in c.contents:
            if u != '\n':
                urls.append(u)
    for url in urls:
        citys.append({'city': url.string, 'url': url.attrs['href']})
    redis.set('citys', json.dumps(citys), 3600 * 24 * 7)
    return citys


def get_redis():
    r = redis.Redis(host='localhost', port=6379)
    return r
