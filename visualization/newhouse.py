import pymongo
import time
from visualization.echarts import charts
import os
from visualization.common import *
from pyecharts.render import make_snapshot
# 使用 snapshot-selenium 渲染图片
from snapshot_selenium import snapshot
from config.configs import *


# 新房数据分析
class newhouse():
    def __init__(self):
        self.path = base_path + sep + "newhouse"
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.charts = charts()
        self.client = pymongo.MongoClient()
        db = newhousedb()
        self.db = self.client[db]
        self.collections = self.db.list_collection_names()
        # 每平米均价
        self.avg_price_square_meter = []
        # 每套房均价
        self.avg_loupan = []
        for city in self.collections:
            self.main_price_range(city)
            self.second_price_range(city)
        self.avg_square_meter(self.collections)
        self.avg_loupan_price(self.collections)
        self.wuye_type_count(self.collections)
        self.huxing_count(self.collections)
        self.square_meter_max_top5(self.collections)
        self.square_meter_min_top5(self.collections)
        self.tag_wordcloud(self.collections)

    # 每平米价位占比
    def main_price_range(self, city):
        match = get_main_price_range(city)
        save_dir = self.path + sep + "main_price_range"
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
                            'main_price': value,
                            'main_price_desc': '元/平(均价)'
                        }
                    ).count()
                )
        bar = self.charts.bar(range_key, range_value, city,
                              main_price_range_template.format(city), "单位: 元/m²")
        make_snapshot(snapshot, bar.render(),
                      img_name.format(save_dir, main_price_range_template.format(city)))
        print("finished {} newhouse main_price_range".format(city))

    # 每套房各价位占比
    def second_price_range(self, city):
        match = get_second_price_range(city)
        range_key = []
        range_value = []
        save_dir = self.path + sep + "second_price_range"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        collection = self.db[city]
        if match:
            for key, value in match.items():
                range_key.append(key + "万")
                range_value.append(
                    collection.find(
                        {
                            'second_price': value,
                        }
                    ).count()
                )
        bar = self.charts.pie_radius(range_key, range_value, second_price_range_template.format(city))
        make_snapshot(snapshot, bar.render(),
                      img_name.format(save_dir, second_price_range_template.format(city)))
        print("finished {} newhouse second_price_range".format(city))

    # 每平米均价
    def avg_square_meter(self, collections):
        save_dir = self.path + sep + "avg_square_meter"
        first_key = []
        second_land_key = []
        second_sea_key = []
        third_key = []
        forth_key = []
        fifth_key = []
        first_value = []
        second_land_value = []
        second_sea_value = []
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
                            'main_price': {
                                '$ne': -1
                            }
                        }
                    },
                    {
                        '$match': {
                            'main_price_desc': '元/平(均价)'
                        }
                    },
                    {
                        '$group': {
                            '_id': 'city',
                            'main_price_avg': {
                                '$avg': '$main_price'
                            }
                        }
                    }
                ]
            ))
            dict = {}
            if average_price:
                dict[city] = int(average_price[0]['main_price_avg'])
                if city in first_level:
                    first_key.append(city)
                    first_value.append(int(average_price[0]['main_price_avg']))
                if city in second_land_level:
                    second_land_key.append(city)
                    second_land_value.append(int(average_price[0]['main_price_avg']))
                if city in second_near_sea_level:
                    second_sea_key.append(city)
                    second_sea_value.append(int(average_price[0]['main_price_avg']))
                if city in third_level:
                    third_key.append(city)
                    third_value.append(int(average_price[0]['main_price_avg']))
                if city in forth_level:
                    forth_key.append(city)
                    forth_value.append(int(average_price[0]['main_price_avg']))
                if city in fifth_level:
                    fifth_key.append(city)
                    fifth_value.append(int(average_price[0]['main_price_avg']))
            self.avg_price_square_meter.append(dict)
        first_bar = self.charts.bar(first_key, first_value, "",
                                    first_level_avg_square_template, temproary_loss)
        make_snapshot(snapshot, first_bar.render(),
                      img_name.format(save_dir, first_level_avg_square_template))
        second_land_bar = self.charts.bar(second_land_key, second_land_value, "",
                                          second_level_land_avg_square_template, temproary_loss)
        make_snapshot(snapshot, second_land_bar.render(), img_name.format(save_dir,
                                                                                       second_level_land_avg_square_template))
        second_sea_bar = self.charts.bar(second_sea_key, second_sea_value, "",
                                         second_level_sea_avg_square_template, temproary_loss)
        make_snapshot(snapshot, second_sea_bar.render(), img_name.format(save_dir,
                                                                                      second_level_sea_avg_square_template))
        third_bar = self.charts.bar(third_key, third_value, "",
                                    third_level_avg_square_template, temproary_loss)
        make_snapshot(snapshot, third_bar.render(),
                      img_name.format(save_dir, third_level_avg_square_template))
        forth_bar = self.charts.bar(forth_key, forth_value, "",
                                    forth_level_avg_square_template, temproary_loss)
        make_snapshot(snapshot, forth_bar.render(),
                      img_name.format(save_dir, forth_level_avg_square_template))
        fifth_bar = self.charts.bar(fifth_key, fifth_value, "",
                                    fifth_level_avg_square_template, temproary_loss)
        make_snapshot(snapshot, fifth_bar.render(),
                      img_name.format(save_dir, fifth_level_avg_square_template))
        print("finish newhouse count avg square meter price")

    # 每套房均价
    def avg_loupan_price(self, collections):
        save_dir = self.path + sep + "avg_loupan"
        first_key = []
        second_land_key = []
        second_sea_key = []
        third_key = []
        forth_key = []
        fifth_key = []
        first_value = []
        second_land_value = []
        second_sea_value = []
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
                            'second_price': {
                                '$ne': -1
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': 'city',
                            'second_price_avg': {
                                '$avg': '$second_price'
                            }
                        }
                    }
                ]
            ))
            dict = {}
            if average_price:
                dict[city] = int(average_price[0]['second_price_avg'])
                if city in first_level:
                    first_key.append(city)
                    first_value.append(int(average_price[0]['second_price_avg']))
                if city in second_land_level:
                    second_land_key.append(city)
                    second_land_value.append(int(average_price[0]['second_price_avg']))
                if city in second_near_sea_level:
                    second_sea_key.append(city)
                    second_sea_value.append(int(average_price[0]['second_price_avg']))
                if city in third_level:
                    third_key.append(city)
                    third_value.append(int(average_price[0]['second_price_avg']))
                if city in forth_level:
                    forth_key.append(city)
                    forth_value.append(int(average_price[0]['second_price_avg']))
                if city in fifth_level:
                    fifth_key.append(city)
                    fifth_value.append(int(average_price[0]['second_price_avg']))
            self.avg_loupan.append(dict)
        first_bar = self.charts.bar(first_key, first_value, "",
                                    first_level_avg_loupan, temproary_loss)
        make_snapshot(snapshot, first_bar.render(), img_name.format(save_dir, first_level_avg_loupan))
        second_land_bar = self.charts.bar(second_land_key, second_land_value, "",
                                          second_level_land_avg_loupan, temproary_loss)
        make_snapshot(snapshot, second_land_bar.render(), img_name.format(save_dir,
                                                                                       second_level_land_avg_loupan))
        second_sea_bar = self.charts.bar(second_sea_key, second_sea_value, "",
                                         second_level_sea_avg_loupan, temproary_loss)
        make_snapshot(snapshot, second_sea_bar.render(), img_name.format(save_dir,
                                                                                      second_level_sea_avg_loupan))
        third_bar = self.charts.bar(third_key, third_value, "",
                                    third_level_avg_loupan, temproary_loss)
        make_snapshot(snapshot, third_bar.render(), img_name.format(save_dir, third_level_avg_loupan))
        forth_bar = self.charts.bar(forth_key, forth_value, "",
                                    forth_level_avg_loupan, temproary_loss)
        make_snapshot(snapshot, forth_bar.render(), img_name.format(save_dir, forth_level_avg_loupan))
        fifth_bar = self.charts.bar(fifth_key, fifth_value, "",
                                    fifth_level_avg_loupan, temproary_loss)
        make_snapshot(snapshot, fifth_bar.render(), img_name.format(save_dir, fifth_level_avg_loupan))
        print("finish count avg loupan price")

    # 物业占比分布图
    def wuye_type_count(self, collections):
        save_dir = self.path + sep + "wuye_type_count"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            wuye_type = list(self.db[city].aggregate(
                [
                    {
                        '$match': {
                            'wuye_type': {
                                '$ne': ''
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': '$wuye_type',
                            'wuye_type_count': {
                                '$sum': 1
                            }
                        }
                    }
                ]
            ))
            wuye_key = [i['_id'] for i in wuye_type]
            wuye_value = [i['wuye_type_count'] for i in wuye_type]
            wuye_bar = self.charts.bar(wuye_key, wuye_value, "",
                                       wuye_type_count_template.format(city), "")
            make_snapshot(snapshot, wuye_bar.render(),
                         img_name.format(save_dir, wuye_type_count_template.format(city)))
            print("finish {} wuye_type_count".format(city))

    # 各户型占比
    def huxing_count(self, collections):
        save_dir = self.path + sep + "huxing_count"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            huxing = list(self.db[city].aggregate(
                [
                    {
                        '$match': {
                            'huxing': {
                                '$ne': ''
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': '$huxing',
                            'huxing_count': {
                                '$sum': 1
                            }
                        }
                    }
                ]
            ))
            huxing_key = [i['_id'] for i in huxing]
            huxing_value = [i['huxing_count'] for i in huxing]
            huxing_bar = self.charts.bar(huxing_key, huxing_value, "",
                                         huxing_count_template.format(city), "")
            make_snapshot(snapshot, huxing_bar.render(),
                          img_name.format(save_dir, huxing_count_template.format(city)))
            print("finish {} huxing_count".format(city))

    # 每平米最贵的top5楼盘
    def square_meter_max_top5(self, collections):
        save_dir = self.path + sep + "square_meter_max_top5"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            max_top5 = list(self.db[city].aggregate(
                [
                    {'$match': {'main_price': {'$ne': -1}, 'main_price_desc': '元/平(均价)'}},
                    {'$sort': {'main_price': -1}},
                    {'$limit': 5},
                    {'$project': {'main_price': 1, 'loupan': 1, '_id': 0}}
                ]
            ))
            if max_top5:
                key = [i['loupan'] for i in max_top5]
                value = [i['main_price'] for i in max_top5]
            max_top5_scatter = self.charts.scatter_visualmap_color(key, value, city,
                                                                   square_price_max_top5.format(city))
            make_snapshot(snapshot, max_top5_scatter.render(),
                          img_name.format(save_dir, square_price_max_top5.format(city)))
            print('finish {} max_top5'.format(city))

    # 每平米最便宜的top5楼盘
    def square_meter_min_top5(self, collections):
        save_dir = self.path + sep + "square_meter_min_top5"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            min_top5 = list(self.db[city].aggregate(
                [
                    {'$match': {'main_price': {'$ne': -1}, 'main_price_desc': '元/平(均价)'}},
                    {'$sort': {'main_price': 1}},
                    {'$limit': 5},
                    {'$project': {'main_price': 1, 'loupan': 1, '_id': 0}}
                ]
            ))
            if min_top5:
                key = [i['loupan'] for i in min_top5]
                value = [i['main_price'] for i in min_top5]
            min_top5_scatter = self.charts.scatter_spliteline(key, value, city,
                                                              square_price_min_top5.format(city))
            make_snapshot(snapshot, min_top5_scatter.render(),
                          img_name.format(save_dir, square_price_min_top5.format(city)))
            print('finish {} min_top5'.format(city))

    # 标签词云
    def tag_wordcloud(self, collections):
        save_dir = self.path + sep + "tag_wordcloud"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            word = {}
            wordcloud = []
            result = list(self.db[city].aggregate(
                [
                    {'$match': {'tag': {'$ne': []}}},
                    {'$project': {'tag': 1, '_id': 0}}
                ]
            ))
            for tag in result:
                for i in tag['tag']:
                    word[i] = 0
            for tag in result:
                for i in tag['tag']:
                    word[i] += 1
            for key, value in word.items():
                wordcloud.append((key, value))
            tag = self.charts.wordcloud_diamond(wordcloud, title='{}市新房热门标签'.format(city))
            make_snapshot(snapshot, tag.render(),
                          img_name.format(save_dir, '{}市新房热门标签'.format(city)))
            print("完成{}市热门标签".format(city))


if __name__ == '__main__':
    new = newhouse()
