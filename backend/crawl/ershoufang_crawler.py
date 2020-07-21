import json
import re
import time
import requests
import datetime
from config import *
from crawl.crawler import LianjiaCrawler
from ershoufang.models import ErShouFang
from utils.html_perser_tools import CloudSkyHtmlParser
from statistic.models import Statistic


class ErShouFangCrawler(LianjiaCrawler):
    ershoufang_all_house_urls = {}

    def __init__(self):
        super().__init__()
        print("start crawling ershoufang")
        redis_connection = get_redis_conn()
        logger.info("city_dict {}".format(self.city_dict))
        for city, city_url in self.city_dict.items():
            logger.info("crawling {} {}".format(city, city_url))
            house_url_ids = []
            total_page = self.get_total_page(city_url)
            for page in range(1, total_page + 1):
                page_url_ids = self.get_per_page_house_url(city_url, page)
                house_url_ids = house_url_ids + page_url_ids
            house_url_ids = list(set(house_url_ids))
            city_house_urls = [ershoufang_house_urls_pattern.format(city_url, id) for id in
                               house_url_ids]
            self.ershoufang_all_house_urls[city] = city_house_urls
            redis_connection.set(city_house_urls_key.format(city),
                                 json.dumps({city: city_house_urls}), cache_one_day)
            self.get_city_house_data(city, city_house_urls)
        redis_connection.set(ershoufang_city_house_urls_key,
                             json.dumps(self.ershoufang_all_house_urls), cache_one_day)
        logger.info("finish crawl ershoufang .")

    # 获取城市二手房数据总页数
    def get_total_page(self, city_url):
        city_url = self.ershoufang_pattern.format(city_url, 1)
        response = requests.get(city_url, headers=self.headers)
        try:
            page = re.findall(re.compile('<ul class="lists" data-mark="list_container" data-info="(.+?)">'),
                              response.text)
            page = int(page[0].split('=')[1])
            if isinstance(page, int):
                return int(int(page) / 30) + 1
            return city_default_max_page
        except Exception:
            logger.warning("get city_max_page error !")
            return city_default_max_page

    # 获取一个城市的单页二手房房源 url
    def get_per_page_house_url(self, city_url, page):
        response = requests.get(self.ershoufang_pattern.format(city_url, page),
                                headers=self.headers)
        url_ids = re.findall(re.compile('<a href="https://m.lianjia.com/{}/ershoufang/(.+?).html"'.format(city_url)),
                             response.text)
        return url_ids

    # 爬取一个城市的二手房数据
    def get_city_house_data(self, city, city_house_urls):
        parser = CloudSkyHtmlParser()
        logger.info("crawling {} .".format(city))
        statistic = {'start_time': datetime.datetime.now()}
        city_house_list = []
        for house_url in city_house_urls:
            try:
                selector_class_names = ['detail_title', 'similar_data',
                                        'house_description big lightblack lazyload_ulog',
                                        'item_list', 'mod_cont fiveline house_intro_mod_cont',
                                        'mod_box house_record', 'info_layer',
                                        'map_marker', 'haofang-wrap']
                response = requests.get(house_url, headers=self.headers)
                kwargs = {'house_url': house_url, 'city': city}
                per_house = parser.get_texts_by_class_name(response.text, selector_class_names)
                if per_house:
                    kwargs['name'] = per_house[0]
                    data = per_house[1].split('\n')
                    if '万' in data[0]:
                        kwargs['total_price'] = parser.match_positive_number(data[0]) * 10000
                    else:
                        kwargs['total_price'] = parser.match_positive_number(data[0])
                    kwargs['unit_type'] = data[1].replace('房型', '') if data[1] else ''
                    kwargs['square'] = parser.match_positive_number(data[2]) if data[2] and (
                            'm²' or '面积' in data[2]) else ''
                data = [x.split('：') for x in per_house[2].strip().split('\n')]
                detail = {}
                for x in data:
                    try:
                        if x and x[0] and x[1]:
                            detail[x[0]] = x[1]
                            kwargs['detail'] = detail if detail else {'detail': 'empty'}
                    except:
                        logger.warning("parse house detail error .")
                        kwargs['detail'] = {'detail': 'empty'}
                        pass
                kwargs['unit_price'] = parser.match_positive_number(data[0][1]) if data[0][1] else -1
                upload_time = data[1][1] if data[1][1] else ''
                upload_time_list = upload_time.split('.')
                if len(upload_time_list) == 3:
                    kwargs['upload_time'] = "{}-{}-{} 00:00:00".format(upload_time_list[0], upload_time_list[1],
                                                                       upload_time_list[2])
                else:
                    kwargs['upload_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
                kwargs['orientation'] = data[2][1] if data[2][1] else ''
                kwargs['floor'] = data[3][1] if data[3][1] else ''
                kwargs['building_type'] = data[4][1] if data[4][1] else ''
                kwargs['elevator'] = data[5][1] if data[5][1] else ''
                kwargs['renovation'] = data[6][1] if data[6][1] else ''
                kwargs['purpose'] = data[7][1] if data[7][1] else ''
                kwargs['ownership'] = data[8][1] if data[8][1] else ''
                kwargs['down_payment_budget'] = data[9][1] if data[9][1] else ''
                kwargs['community'] = data[10][1] if data[10][1] else ''
                data = [x.split(':') for x in per_house[3].strip().split('\n')]
                room_info = {}
                for x in data:
                    try:
                        if x and x[0] and x[1]:
                            room_info[x[0]] = x[1]
                            kwargs['room_info'] = room_info if room_info else {"room_info": "empty"}
                    except Exception:
                        logger.warning("room_info parse error .")
                        kwargs['room_info'] = ""
                        pass
                kwargs['introduction'] = per_house[4].strip()
                if per_house[5] and '房源动态' in per_house[5]:
                    kwargs['trends'] = per_house[5].replace('\n', '')
                else:
                    kwargs['trends'] = per_house[5]
                kwargs['basic_attributes'] = per_house[6]
                kwargs['position'] = per_house[7]
                kwargs['highlight'] = per_house[8].replace('好房亮点', '').strip()
                img_class_names = ['vr_box', 'box_col']
                img_data = parser.get_img_by_class_name(response.text, img_class_names)
                kwargs['img_url'] = img_data[0] if img_data else ''
                city_house_list.append(ErShouFang(**kwargs))
            except Exception:
                logger.warning("key error .")
        ErShouFang.objects.bulk_create(city_house_list)
        statistic['end_time'] = datetime.datetime.now()
        statistic['total'] = len(city_house_urls)
        statistic['city'] = city
        statistic['type'] = 'ershoufang'
        statistic['cost_time'] = str(statistic['end_time'] - statistic['start_time'])
        Statistic.objects.create(**statistic)
        logger.info("finish city {}".format(city))
