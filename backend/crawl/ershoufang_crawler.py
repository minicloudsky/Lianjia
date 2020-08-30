import datetime
import json
import os
import re
import time
from multiprocessing import Pool
import requests
from config import *
from crawl.crawler import LianjiaCrawler
from ershoufang.models import ErShouFang
from statistic.models import Statistic
from utils.html_perser_tools import CloudSkyHtmlParser


class ErShouFangCrawler(LianjiaCrawler):
    ershoufang_all_house_urls = {}

    def __init__(self):
        super().__init__()
        print("start crawling ershoufang")
        redis_connection = get_redis_conn()
        print(self.city_dict)
        count = 0
        temp_dict = {}
        process_pool = Pool(int(len(self.city_dict.keys()) / 10) + 1)
        for city, city_url in self.city_dict.items():
            # temp_dict[city] = city_url
            # count += 1
            # if count % 10 == 0:
            #     process_pool.apply_async(
            #         self.get_process_houses, args=(temp_dict,))
            #     temp_dict = {}
            self.get_city_ershoufang(city, city_url)
        # process_pool.close()
        # process_pool.join()
        # print('等待所有爬虫子进程完成。')

        redis_connection.set(ershoufang_city_house_urls_key,
                             json.dumps(self.ershoufang_all_house_urls), cache_one_day)
        logger.info("finish crawl ershoufang .")

    def get_process_houses(self, process_city_dict):
        for city, city_url in process_city_dict.items():
            self.get_city_ershoufang(city, city_url)

    # 开启多进程，每个城市开启一个进程进行抓取
    def get_city_ershoufang(self, city, city_url):
        redis_connection = get_redis_conn()
        house_url_ids = []
        total_page = self.get_total_page(city_url)
        logger.info("start get {} house url.".format(city))
        for page in range(1, total_page + 1):
            page_url_ids = self.get_per_page_house_url(city_url, page)
            house_url_ids = house_url_ids + page_url_ids
            print("getting page: {}".format(page))
        house_url_ids = list(set(house_url_ids))
        logger.info(" {} total house urls: {}.".format(city, len(house_url_ids)))
        city_house_urls = [ershoufang_house_urls_pattern.format(city_url, id) for id in
                           house_url_ids]
        self.ershoufang_all_house_urls[city] = city_house_urls
        redis_connection.set(city_house_urls_key.format(city),
                             json.dumps({city: city_house_urls}), cache_one_day)
        self.get_city_house_data(city, house_url_ids)

    # 获取城市二手房数据总页数
    def get_total_page(self, city_url):
        city_url = self.ershoufang_pattern.format(city_url, 1)
        response = self.request(city_url)
        try:
            page = re.findall(re.compile('<ul class="lists" data-mark="list_container" data-info="(.+?)">'),
                              response.text)
            page = int(page[0].split('=')[1])
            if isinstance(page, int):
                return int(int(page) / 30) + 1
            return city_default_max_page
        except Exception:
            return city_default_max_page

    # 获取一个城市的单页二手房房源 url
    def get_per_page_house_url(self, city_url, page):
        response = self.request(self.ershoufang_pattern.format(city_url, page))
        url_ids = re.findall(re.compile('<a href="https://m.lianjia.com/{}/ershoufang/(.+?).html"'.format(city_url)),
                             response.text)
        return url_ids

    # 爬取一个城市的二手房数据
    def get_city_house_data(self, city, house_url_ids):
        parser = CloudSkyHtmlParser()
        logger.info("任务: {} 进程: {} crawling  .".format(city, os.getpid()))
        statistic = {'start_time': datetime.datetime.now()}
        city_house_list = []
        for house_url_id in house_url_ids:
            selector_class_names = ['detail_title', 'similar_data',
                                    'house_description big lightblack lazyload_ulog',
                                    'item_list', 'mod_cont fiveline house_intro_mod_cont',
                                    'mod_box house_record', 'info_layer',
                                    'map_marker', 'haofang-wrap']
            response = self.request(ershoufang_house_urls_pattern.format(house_url_id, id))
            kwargs = {'house_url_id': house_url_id, 'city': city}
            try:
                per_house = parser.get_texts_by_class_name(
                    response.text, selector_class_names)
                if per_house:
                    kwargs['name'] = per_house[0] if per_house[0] else ''
                    data = per_house[1].split('\n') if per_house[1] else ''
                    if '万' in data[0]:
                        kwargs['total_price'] = parser.match_positive_number(
                            data[0] if data[0] else -1) * 10000
                    else:
                        kwargs['total_price'] = parser.match_positive_number(
                            data[0] if data[0] else -1)
                    kwargs['unit_type'] = data[1].replace('房型', '') if data and len(data) >= 2 else ''
                    kwargs['square'] = parser.match_positive_number(data[2] if len(data) >= 2 else "") if data[2] and (
                            'm²' or '面积' in data[2]) else ''
                data = [x.split('：') for x in per_house[2].strip().split('\n')]
                detail = {}
                for x in data:
                    try:
                        if x and x[0] and x[1]:
                            detail[x[0]] = x[1]
                            kwargs['detail'] = detail if detail else {
                                'detail': 'empty'}
                    except:
                        # logger.warning(
                        #     "{} {} parse house detail error .".format(house_url, os.getpid()))
                        kwargs['detail'] = {'detail': 'empty'}
                        pass
                kwargs['unit_price'] = parser.match_positive_number(
                    data[0][1]) if data[0][1] else -1
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
                            kwargs['room_info'] = room_info if room_info else {
                                "room_info": "empty"}
                    except Exception:
                        # logger.warning(
                        #     "{} 进程: {} room_info parse error .".format(house_url, os.getpid()))
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
                img_data = parser.get_img_by_class_name(
                    response.text, img_class_names)
                kwargs['img_url'] = img_data[0] if img_data else ''
            except Exception as e:
                logger.warn("----parse html error {}".format(e))
                pass
            city_house_list.append(ErShouFang(**kwargs))
            logger.info("-------二手房-", ErShouFang(**kwargs))
        logger.info("{}一共有 {} 套二手房源".format(city, len(city_house_list)))
        ErShouFang.objects.bulk_create(city_house_list)
        logger.info("{} 房源插入成功".format(city))
        statistic['end_time'] = datetime.datetime.now()
        statistic['total'] = len(house_url_ids)
        statistic['city'] = city
        statistic['type'] = 'ershoufang'
        statistic['cost_time'] = str(
            statistic['end_time'] - statistic['start_time'])
        Statistic.objects.create(**statistic)
        logger.info("任务: {} 进程: {} finish .".format(city, os.getpid()))
