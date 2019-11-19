import pymongo
import time
from visualization.echarts import charts
import os
from visualization.common import *
from pyecharts.render import make_snapshot
# 使用 snapshot-selenium 渲染图片
from snapshot_selenium import snapshot
from visualization.lang import *
from config.configs import *
from .common import *


class ershoufang():
    unit_price_template = '{}市二手房每平米楼盘价位占比分布图'
    total_price_template = '{}市二手房每套房价位占比分布图'
    yuan_per_square = '元/平'
    ten_thousand_per_loupan = '万/套'
    square_price_max_top5 = '{}市二手房每平米最贵top5小区'
    square_price_min_top5 = '{}市二手房每平米最便宜top5小区'

    def __init__(self):
        self.path = base_path + sep + "ershoufang"
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.charts = charts()
        self.client = pymongo.MongoClient()
        db = ershoufangdb()
        self.db = self.client[db]
        self.collections = self.db.list_collection_names()
        # 每平米均价
        self.avg_price_square_meter = []
        # 每套房均价
        self.avg_loupan = []
        self.queue = self.collections
        for city in self.collections:
            self.unit_price_range(city)
            self.total_price_range(city)
        self.avg_square_meter(self.collections)
        self.avg_loupan_price(self.collections)
        self.square_meter_max_top5(self.collections)
        self.square_meter_min_top5(self.collections)
        self.xiaoqu_wordcloud(self.collections)
        self.position_wordcloud(self.collections)

    # 每平米价位占比
    def unit_price_range(self, city):
        match = get_unit_price_range(city)
        save_dir = self.path + sep + "unit_price_range"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        collection = self.db[city]
        range_key = []
        range_value = []
        if match:
            for key, value in match.items():
                range_key.append(key)
                range_value.append(
                    collection.find(
                        {
                            'unit_price': value,
                        }
                    ).count()
                )
        bar = self.charts.bar(range_key, range_value, city,
                              self.unit_price_template.format(city), per_square)
        make_snapshot(snapshot, bar.render(),
                      img_name.format(save_dir, ershoufang_unit_price.format(city)),
                      delay=5)
        print("完成 " + ershoufang_unit_price.format(city))

    # 每套房各价位占比
    def total_price_range(self, city):
        match = get_total_price_range(city)
        range_key = []
        range_value = []
        save_dir = self.path + sep + "total_price_range"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        collection = self.db[city]
        if match:
            for key, value in match.items():
                range_key.append(key + "万")
                range_value.append(
                    collection.find(
                        {
                            'total_price': value,
                        }
                    ).count()
                )
        bar = self.charts.pie_radius(range_key, range_value, self.total_price_template.format(city))
        make_snapshot(snapshot, bar.render(),
                      img_name.format(save_dir, ershoufang_total_price.format(city)))
        print("完成" + ershoufang_total_price.format(city))

    # 每平米均价
    def avg_square_meter(self, collections):
        save_dir = self.path + sep + "avg_square_meter"
        first_key = []
        new_first_key = []
        second_key = []
        third_key = []
        forth_key = []
        fifth_key = []
        first_value = []
        new_first_value = []
        second_value = []
        third_value = []
        forth_value = []
        fifth_value = []
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            average_price = list(self.db[city].aggregate(
                [
                    {
                        '$match': {
                            'unit_price': {
                                '$ne': -1
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': 'city',
                            'unit_price_avg': {
                                '$avg': '$unit_price'
                            }
                        }
                    }
                ]
            ))
            dict = {}
            if average_price:
                dict[city] = int(average_price[0]['unit_price_avg'])
                if city in lianjia_citys['first']:
                    first_key.append(city)
                    first_value.append(int(average_price[0]['unit_price_avg']))
                if city in lianjia_citys['new_first']:
                    new_first_key.append(city)
                    new_first_value.append(int(average_price[0]['unit_price_avg']))
                if city in lianjia_citys['second']:
                    second_key.append(city)
                    second_value.append(int(average_price[0]['unit_price_avg']))
                if city in lianjia_citys['third']:
                    third_key.append(city)
                    third_value.append(int(average_price[0]['unit_price_avg']))
                if city in lianjia_citys['forth']:
                    forth_key.append(city)
                    forth_value.append(int(average_price[0]['unit_price_avg']))
                if city in lianjia_citys['fifth']:
                    fifth_key.append(city)
                    fifth_value.append(int(average_price[0]['unit_price_avg']))
            self.avg_price_square_meter.append(dict)
        first_bar = self.charts.bar(first_key, first_value, "", first_ershoufang_square_avg, self.yuan_per_square)
        make_snapshot(snapshot, first_bar.render(),
                      img_name.format(save_dir, first_ershoufang_square_avg, ))
        new_first_bar = self.charts.bar(new_first_key[:10], new_first_value[:10], "",
                                        new_first_ershoufang_square_avg, self.yuan_per_square)
        make_snapshot(snapshot, new_first_bar.render(),
                      img_name.format(save_dir, new_first_ershoufang_square_avg, ))
        new_first_bar2 = self.charts.bar(new_first_key[10:], new_first_value[10:], "",
                                         new_first_ershoufang_square_avg_2, self.yuan_per_square)
        make_snapshot(snapshot, new_first_bar2.render(),
                      img_name.format(save_dir, new_first_ershoufang_square_avg_2, ))
        second_bar = self.charts.bar(second_key[:10], second_value[:10], "",
                                     second_ershoufang_square_avg, self.yuan_per_square)
        make_snapshot(snapshot, second_bar.render(), img_name.format(save_dir,
                                                                     second_ershoufang_square_avg))
        second_bar2 = self.charts.bar(second_key[10:20], second_value[10:20], "",
                                      second_ershoufang_square_avg_2, self.yuan_per_square)
        make_snapshot(snapshot, second_bar2.render(), img_name.format(save_dir,
                                                                      second_ershoufang_square_avg_2))
        second_bar3 = self.charts.bar(second_key[20:], second_value[20:], "",
                                      second_ershoufang_square_avg_3, self.yuan_per_square)
        make_snapshot(snapshot, second_bar3.render(), img_name.format(save_dir,
                                                                      second_ershoufang_square_avg_3))
        third_bar = self.charts.bar(third_key[:10], third_value[:10], "",
                                    third_ershoufang_square_avg, self.yuan_per_square)
        make_snapshot(snapshot, third_bar.render(), img_name.format(save_dir, third_ershoufang_square_avg))
        third_bar2 = self.charts.bar(third_key[10:20], third_value[10:20], "",
                                     third_ershoufang_square_avg_2, self.yuan_per_square)
        make_snapshot(snapshot, third_bar2.render(),
                      img_name.format(save_dir, third_ershoufang_square_avg_2))
        third_bar3 = self.charts.bar(third_key[20:], third_value[20:], "",
                                     third_ershoufang_square_avg_3, self.yuan_per_square)
        make_snapshot(snapshot, third_bar3.render(),
                      img_name.format(save_dir, third_ershoufang_square_avg_3))
        forth_bar = self.charts.bar(forth_key[:10], forth_value[:10], "",
                                    forth_ershoufang_suqare_avg, self.yuan_per_square)
        make_snapshot(snapshot, forth_bar.render(), img_name.format(save_dir, forth_ershoufang_suqare_avg))
        forth_bar2 = self.charts.bar(forth_key[10:20], forth_value[10:20], "",
                                     forth_ershoufang_suqare_avg_2, self.yuan_per_square)
        make_snapshot(snapshot, forth_bar2.render(),
                      img_name.format(save_dir, forth_ershoufang_suqare_avg_2))
        forth_bar3 = self.charts.bar(forth_key[20:], forth_value[20:], "",
                                     forth_ershoufang_suqare_avg_3, self.yuan_per_square)
        make_snapshot(snapshot, forth_bar3.render(),
                      img_name.format(save_dir, forth_ershoufang_suqare_avg_3))
        fifth_bar = self.charts.bar(fifth_key, fifth_value, "",
                                    fifth_ershoufang_square_avg, self.yuan_per_square)
        make_snapshot(snapshot, fifth_bar.render(), img_name.format(save_dir, fifth_ershoufang_square_avg))
        print("完成链家二手房各城市每平米均价作图")

    # 每套房均价
    def avg_loupan_price(self, collections):
        save_dir = self.path + sep + "avg_loupan"
        first_key = []
        new_first_key = []
        second_key = []
        third_key = []
        forth_key = []
        fifth_key = []
        first_value = []
        new_first_value = []
        second_value = []
        third_value = []
        forth_value = []
        fifth_value = []
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            average_price = list(self.db[city].aggregate(
                [
                    {
                        '$match': {
                            'total_price': {
                                '$ne': -1
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': 'city',
                            'total_price_avg': {
                                '$avg': '$total_price'
                            }
                        }
                    }
                ]
            ))

            dict = {}
            if average_price:
                dict[city] = int(average_price[0]['total_price_avg'])
                if city in lianjia_citys['first']:
                    first_key.append(city)
                    first_value.append(int(average_price[0]['total_price_avg']))
                if city in lianjia_citys['new_first']:
                    new_first_key.append(city)
                    new_first_value.append(int(average_price[0]['total_price_avg']))
                if city in lianjia_citys['second']:
                    second_key.append(city)
                    second_value.append(int(average_price[0]['total_price_avg']))
                if city in lianjia_citys['third']:
                    third_key.append(city)
                    third_value.append(int(average_price[0]['total_price_avg']))
                if city in lianjia_citys['forth']:
                    forth_key.append(city)
                    forth_value.append(int(average_price[0]['total_price_avg']))
                if city in lianjia_citys['fifth']:
                    fifth_key.append(city)
                    fifth_value.append(int(average_price[0]['total_price_avg']))
            self.avg_price_square_meter.append(dict)
        first_bar = self.charts.bar(first_key, first_value, "", first_ershoufang_loupan_avg,
                                    self.ten_thousand_per_loupan)
        make_snapshot(snapshot, first_bar.render(),
                      img_name.format(save_dir, first_ershoufang_loupan_avg, ))
        new_first_bar = self.charts.bar(new_first_key[:10], new_first_value[:10], "",
                                        new_first_ershoufang_loupan_avg, self.ten_thousand_per_loupan)
        make_snapshot(snapshot, new_first_bar.render(),
                      img_name.format(save_dir, new_first_ershoufang_loupan_avg, ))
        new_first_bar2 = self.charts.bar(new_first_key[10:], new_first_value[10:], "",
                                         new_first_ershoufang_loupan_avg_2, self.ten_thousand_per_loupan)
        make_snapshot(snapshot, new_first_bar2.render(),
                      img_name.format(save_dir, new_first_ershoufang_loupan_avg_2, ))
        second_bar = self.charts.bar(second_key[:10], second_value[:10], "",
                                     second_ershoufang_loupan_avg, self.ten_thousand_per_loupan)
        make_snapshot(snapshot, second_bar.render(), img_name.format(save_dir,
                                                                     second_ershoufang_loupan_avg))
        second_bar2 = self.charts.bar(second_key[10:20], second_value[10:20], "",
                                      second_ershoufang_loupan_avg_2, self.ten_thousand_per_loupan)
        make_snapshot(snapshot, second_bar2.render(), img_name.format(save_dir,
                                                                      second_ershoufang_loupan_avg_2))
        second_bar3 = self.charts.bar(second_key[20:], second_value[20:], "",
                                      second_ershoufang_loupan_avg_3, self.ten_thousand_per_loupan)
        make_snapshot(snapshot, second_bar3.render(), img_name.format(save_dir,
                                                                      second_ershoufang_loupan_avg_3))
        third_bar = self.charts.bar(third_key[:10], third_value[:10], "",
                                    third_ershoufang_loupan_avg, self.ten_thousand_per_loupan)
        make_snapshot(snapshot, third_bar.render(), img_name.format(save_dir, third_ershoufang_loupan_avg))
        third_bar2 = self.charts.bar(third_key[10:20], third_value[10:20], "",
                                     third_ershoufang_loupan_avg_2, self.ten_thousand_per_loupan)
        make_snapshot(snapshot, third_bar2.render(),
                      img_name.format(save_dir, third_ershoufang_loupan_avg_2))
        third_bar3 = self.charts.bar(third_key[20:], third_value[20:], "",
                                     third_ershoufang_loupan_avg_3, self.ten_thousand_per_loupan)
        make_snapshot(snapshot, third_bar3.render(),
                      img_name.format(save_dir, third_ershoufang_loupan_avg_3))
        forth_bar = self.charts.bar(forth_key[:10], forth_value[:10], "",
                                    forth_ershoufang_loupan_avg, self.ten_thousand_per_loupan)
        make_snapshot(snapshot, forth_bar.render(), img_name.format(save_dir, forth_ershoufang_loupan_avg))
        forth_bar2 = self.charts.bar(forth_key[10:20], forth_value[10:20], "",
                                     forth_ershoufang_loupan_avg_2, self.ten_thousand_per_loupan)
        make_snapshot(snapshot, forth_bar2.render(),
                      img_name.format(save_dir, forth_ershoufang_loupan_avg_2))
        forth_bar3 = self.charts.bar(forth_key[20:], forth_value[20:], "",
                                     forth_ershoufang_loupan_avg_3, self.ten_thousand_per_loupan)
        make_snapshot(snapshot, forth_bar3.render(),
                      img_name.format(save_dir, forth_ershoufang_loupan_avg_3))
        fifth_bar = self.charts.bar(fifth_key, fifth_value, "",
                                    fifth_ershoufang_loupan_avg, self.ten_thousand_per_loupan)
        make_snapshot(snapshot, fifth_bar.render(), img_name.format(save_dir, fifth_ershoufang_loupan_avg))
        print("完成链家各城市二手房每套均价作图")

    # 每平米最贵的top5楼盘
    def square_meter_max_top5(self, collections):
        save_dir = self.path + "" + sep + "square_meter_max_top5"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            max_top5 = list(self.db[city].aggregate(
                [
                    {'$match': {'unit_price': {'$ne': -1}}},
                    {'$sort': {'unit_price': -1}},
                    {'$limit': 5},
                    {'$project': {'unit_price': 1, 'xiaoqu_name': 1, '_id': 0, 'position': 1}}
                ]
            ))
            if max_top5:
                if max_top5[0]['xiaoqu_name'] != '':
                    key = [i['xiaoqu_name'] for i in max_top5]
                else:
                    key = [i['position'] for i in max_top5]
                value = [i['unit_price'] for i in max_top5]
            max_top5_scatter = self.charts.scatter_spliteline(key, value, city,
                                                              self.square_price_max_top5.format(city))
            make_snapshot(snapshot, max_top5_scatter.render(),
                          img_name.format(save_dir, self.square_price_max_top5.format(city)))
            print(hot_xiaoqu_ershoufang.format(city))

    # 每平米最便宜的top5楼盘
    def square_meter_min_top5(self, collections):
        save_dir = self.path + sep + "square_meter_min_top5"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            min_top5 = list(self.db[city].aggregate(
                [
                    {'$match': {'unit_price': {'$ne': -1}}},
                    {'$sort': {'unit_price': 1}},
                    {'$limit': 5},
                    {'$project': {'unit_price': 1, 'xiaoqu_name': 1, '_id': 0, 'position': 1}}
                ]
            ))
            if min_top5:
                if min_top5[0]['xiaoqu_name'] != '':
                    key = [i['xiaoqu_name'] for i in min_top5]
                else:
                    key = [i['position'] for i in min_top5]
                value = [i['unit_price'] for i in min_top5]
            min_top5_scatter = self.charts.scatter_visualmap_color(key, value, city,
                                                                   self.square_price_min_top5.format(city))
            make_snapshot(snapshot, min_top5_scatter.render(),
                          img_name.format(save_dir, self.square_price_min_top5.format(city)))
            print('完成 {} 每平米最便宜top5小区作图'.format(city))

    # 热门小区词云
    def xiaoqu_wordcloud(self, collections):
        save_dir = self.path + "" + sep + "xiaoqu_wordcloud"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            xiaoqu = {}
            wordcloud = []
            result = list(self.db[city].aggregate(
                [
                    {'$match': {'xiaoqu_name': {'$ne': ''}}},
                    {'$project': {'xiaoqu_name': 1, '_id': 0}},
                ]
            ))
            for x in result:
                xiaoqu[x['xiaoqu_name']] = 0
            for x in result:
                xiaoqu[x['xiaoqu_name']] += 1
            for key, value in xiaoqu.items():
                wordcloud.append((key, value))
            xiaoqu_wordcloud = self.charts.wordcloud_diamond(wordcloud, title='{}市二手房热门小区'.format(city))
            make_snapshot(snapshot, xiaoqu_wordcloud.render(),
                          img_name.format(save_dir, '{}市二手房热门小区'.format(city)))
            print("完成{}市热门小区词云".format(city))

    # 热门地段词云
    def position_wordcloud(self, collections):
        save_dir = self.path + sep + "position_wordcloud"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            position = {}
            wordcloud = []
            result = list(self.db[city].aggregate(
                [
                    {'$match': {'position': {'$ne': ''}}},
                    {'$project': {'position': 1, '_id': 0}},
                ]
            ))
            for x in result:
                position[x['position']] = 0
            for x in result:
                position[x['position']] += 1
            for key, value in position.items():
                wordcloud.append((key, value))
            position_wordcloud = self.charts.wordcloud_diamond(wordcloud, title='{}市二手房热门地段'.format(city))
            make_snapshot(snapshot, position_wordcloud.render(),
                          img_name.format(save_dir, '{}市二手房热门地段'.format(city)))
            print("完成{}市二手房热门地段词云".format(city))


if __name__ == '__main__':
    house = ershoufang()
