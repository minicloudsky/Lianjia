from visualization.common import *
import os
from visualization.echarts import charts
from pyecharts.render import make_snapshot
# 使用 snapshot-selenium 渲染图片
from snapshot_selenium import snapshot
from config.configs import *


class rent():
    yuan_per_square = '元/套'

    def __init__(self):
        self.path = base_path + sep + "rent"
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.charts = charts()
        self.client = pymongo.MongoClient()
        db = rentdb()
        self.db = self.client[db]
        self.collections = self.db.list_collection_names()
        self.avg_price = []
        self.source_percentage(self.collections)
        self.brandtop5_avg_price(self.collections)
        self.avg_price_rent(self.collections)
        self.rent_max_top5(self.collections)
        self.rent_min_top5(self.collections)
        self.tag_wordcloud(self.collections)

    #  每个品牌房源占比
    def source_percentage(self, collections):
        save_dir = self.path + sep + "source_percentage"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            key = []
            value = []
            result = list(self.db[city].aggregate(
                [{'$match': {'brand': {'$ne': ''}}},
                 {'$group': {'_id': '$brand',
                             'brand_count': {
                                 '$sum': 1
                             }}},
                 {'$sort': {'brand_count': -1}}
                 ]
            ))
            if result:
                if len(result) > 7:
                    six = result[:7]
                    key = [i['_id'] for i in six]
                    value = [i['brand_count'] for i in six]
                    other = 0
                    for i in result[7:]:
                        other += i['brand_count']
                    key.append('其他房源')
                    value.append(other)
                else:
                    key = [i['_id'] for i in result]
                    value = [i['brand_count'] for i in result]
            rose = self.charts.pie_rosetype(key, value, '{}市链家租房来源'.format(city))
            make_snapshot(snapshot, rose.render(),
                          img_name.format(save_dir, '{}市链家租房来源'.format(city)))
            print("完成{}市租房来源作图".format(city))

    # 房源占比最高的top5均价
    def brandtop5_avg_price(self, collections):
        save_dir = self.path + sep + "brand_avg_price"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            key = []
            value = []
            result = list(self.db[city].aggregate(
                [{'$match': {'brand': {'$ne': ''}}},
                 {'$group': {'_id': '$brand',
                             'brand_count': {
                                 '$sum': 1
                             },
                             'avg_price': {'$avg': '$price'}
                             }},
                 {'$sort': {'avg_price': -1}},
                 {'$limit': 5}
                 ]
            ))
            if result:
                for i in result:
                    key.append('{}均价{}元'.format(i['_id'], int(i['avg_price'])))
                    value.append(int(i['avg_price']))
            funnel = self.charts.funnel_label_inside(key, value, '{}市房源占比最高平台top5均价'.format(city))
            make_snapshot(snapshot, funnel.render(),
                          img_name.format(save_dir, '{}市房源占比最高平台top5均价'.format(city)))
            print("完成{}市房源占比最高平台top5均价作图".format(city))

    # 每平米均价
    def avg_price_rent(self, collections):
        save_dir = self.path + sep + "avg_price"
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
                            'price': {
                                '$ne': -1
                            }
                        }
                    },
                    {
                        '$group': {
                            '_id': 'city',
                            'avg_price': {
                                '$avg': '$price'
                            }
                        }
                    }
                ]
            ))
            dict = {}
            if average_price:
                dict[city] = int(average_price[0]['avg_price'])
                if city in lianjia_citys['first']:
                    first_key.append(city)
                    first_value.append(int(average_price[0]['avg_price']))
                if city in lianjia_citys['new_first']:
                    new_first_key.append(city)
                    new_first_value.append(int(average_price[0]['avg_price']))
                if city in lianjia_citys['second']:
                    second_key.append(city)
                    second_value.append(int(average_price[0]['avg_price']))
                if city in lianjia_citys['third']:
                    third_key.append(city)
                    third_value.append(int(average_price[0]['avg_price']))
                if city in lianjia_citys['forth']:
                    forth_key.append(city)
                    forth_value.append(int(average_price[0]['avg_price']))
                if city in lianjia_citys['fifth']:
                    fifth_key.append(city)
                    fifth_value.append(int(average_price[0]['avg_price']))
            self.avg_price.append(dict)
        first_bar = self.charts.bar(first_key, first_value, "", '一线城市租房均价', self.yuan_per_square)
        make_snapshot(snapshot, first_bar.render(), img_name.format(save_dir, '一线城市租房均价', ))
        new_first_bar = self.charts.bar(new_first_key[:10], new_first_value[:10], "",
                                        '新一线城市租房均价(1)', self.yuan_per_square)
        make_snapshot(snapshot, new_first_bar.render(), img_name.format(save_dir, '新一线城市租房均价(1)', ))
        new_first_bar2 = self.charts.bar(new_first_key[10:], new_first_value[10:], "",
                                         '新一线城市二手房租房均价(2)', self.yuan_per_square)
        make_snapshot(snapshot, new_first_bar2.render(), img_name.format(save_dir, '新一线城市租房均价(2)', ))
        second_bar = self.charts.bar(second_key[:10], second_value[:10], "",
                                     '二线城市租房均价(1)', self.yuan_per_square)
        make_snapshot(snapshot, second_bar.render(), img_name.format(save_dir,
                                                                     '二线城市租房均价(1)'))
        second_bar2 = self.charts.bar(second_key[10:20], second_value[10:20], "",
                                      '二线城市租房均价(2)', self.yuan_per_square)
        make_snapshot(snapshot, second_bar2.render(), img_name.format(save_dir,
                                                                      '二线城市租房均价(2)'))
        second_bar3 = self.charts.bar(second_key[20:], second_value[20:], "",
                                      '二线城市租房均价(3)', self.yuan_per_square)
        make_snapshot(snapshot, second_bar3.render(), img_name.format(save_dir,
                                                                      '二线城市租房均价(3)'))
        third_bar = self.charts.bar(third_key[:10], third_value[:10], "",
                                    '三线城市租房均价(1)', self.yuan_per_square)
        make_snapshot(snapshot, third_bar.render(), img_name.format(save_dir, '三线城市租房均价(1)'))
        third_bar2 = self.charts.bar(third_key[10:20], third_value[10:20], "",
                                     '三线城市租房均价(2)', self.yuan_per_square)
        make_snapshot(snapshot, third_bar2.render(), img_name.format(save_dir, '三线城市租房均价(2)'))
        third_bar3 = self.charts.bar(third_key[20:], third_value[20:], "",
                                     '三线城市租房均价(3)', self.yuan_per_square)
        make_snapshot(snapshot, third_bar3.render(), img_name.format(save_dir, '三线城市租房均价(3)'))
        forth_bar = self.charts.bar(forth_key[:10], forth_value[:10], "",
                                    '四线城市租房均价(1)', self.yuan_per_square)
        make_snapshot(snapshot, forth_bar.render(), img_name.format(save_dir, '四线城市租房均价(1)'))
        forth_bar2 = self.charts.bar(forth_key[10:20], forth_value[10:20], "",
                                     '四线城市租房均价(2)', self.yuan_per_square)
        make_snapshot(snapshot, forth_bar2.render(), img_name.format(save_dir, '四线城市租房均价(2)'))
        forth_bar3 = self.charts.bar(forth_key[20:], forth_value[20:], "",
                                     '四线城市租房均价(3)', self.yuan_per_square)
        make_snapshot(snapshot, forth_bar3.render(), img_name.format(save_dir, '四线城市租房均价(3)'))
        fifth_bar = self.charts.bar(fifth_key, fifth_value, "",
                                    '五线城市租房均价', self.yuan_per_square)
        make_snapshot(snapshot, fifth_bar.render(), img_name.format(save_dir, '五线城市租房均价'))
        print("完成二手房租房均价作图")

    # 租房最贵top5
    def rent_max_top5(self, collections):
        save_dir = self.path + sep + "rent_max_top5"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            key = []
            value = []
            max_top5 = list(self.db[city].aggregate(
                [{'$match': {'price': {'$ne': -1}, 'house': {'$ne': ''}}},
                 {'$sort': {'price': -1}},
                 {'$project': {'price': 1, 'house': 1, '_id': 0}},
                 {'$limit': 5}
                 ]
            ))
            if max_top5:
                key = [i['house'].split(' ')[0] for i in max_top5]
                value = [i['price'] for i in max_top5]
            min_top5_scatter = self.charts.scatter_visualmap_color(key, value, city,
                                                                   '{}市租房价格最高top5'.format(city))
            make_snapshot(snapshot, min_top5_scatter.render(),
                          img_name.format(save_dir, '{}市租房价格最高top5'.format(city)))
            print('完成 {} 市租房价格最高top5作图'.format(city))

    # 租房最低top5
    def rent_min_top5(self, collections):
        save_dir = self.path + sep + "rent_min_top5"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for city in collections:
            key = []
            value = []
            min_top5 = list(self.db[city].aggregate(
                [{'$match': {'price': {'$ne': -1}, 'house': {'$ne': ''}}},
                 {'$sort': {'price': 1}},
                 {'$project': {'price': 1, 'house': 1, '_id': 0}},
                 {'$limit': 5}
                 ]
            ))
            if min_top5:
                key = [i['house'].split(' ')[0] for i in min_top5]
                value = [i['price'] for i in min_top5]
            min_top5_scatter = self.charts.scatter_spliteline(key, value, city,
                                                              '{}市租房价格最低top5'.format(city))
            print(img_name.format(save_dir, '{}市租房价格最低top5'.format(city)))
            make_snapshot(snapshot, min_top5_scatter.render(),
                          img_name.format(save_dir, '{}市租房价格最低top5'.format(city)))
            print('完成 {} 市租房价格最低top5作图'.format(city))

    # 租房标签词云
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
            tag = self.charts.wordcloud_diamond(wordcloud, title='{}市租房热门标签'.format(city))
            make_snapshot(snapshot, tag.render(),
                          img_name.format(save_dir, '{}市租房热门标签'.format(city)))
            print("完成{}市租房热门标签".format(city))


if __name__ == '__main__':
    house = rent()
