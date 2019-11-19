from lianjia.constants import *
import os
from visualization.common import base_path

from config.configs import *


class newhouse_list():
    def __init__(self, city, analysis):
        data = []
        self.city = city
        self.analysis = analysis
        self.img_base_path = sep + 'static' + sep + 'newhouse'
        self.result = {
            1: self.main_price_range(city),
            2: self.second_price_range(city),
            3: self.avg_square_meter(city),
            4: self.avg_loupan_price(city),
            5: self.wuye_type_count(city),
            6: self.huxing_count(city),
            7: self.square_meter_max_top5(city),
            8: self.square_meter_min_top5(city),
            9: self.tag_wordcloud(city)
        }

    # 返回数据给前端
    def parse(self):
        return self.result[self.analysis]

    # 每平米价位占比
    def main_price_range(self, city):
        city_map = get_city_map('newhouse')
        data = []
        data.append(
            self.img_base_path + sep + 'main_price_range' + sep + '{}市新房每平米楼盘价位占比分布图.gif'.format(city_map[city]))
        return data

    # 每套房各价位占比
    def second_price_range(self, city):
        city_map = get_city_map('newhouse')
        data = []
        data.append(self.img_base_path + sep + 'second_price_range' + sep + '{}市每套新房价位占比分布图.gif'.format(city_map[city]))
        return data

    # 每平米均价
    def avg_square_meter(self, city):
        img_list = [
            self.img_base_path + sep + 'avg_square_meter' + sep + '链家部分一线城市及新一线城市新房每平米均价.gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '链家部分二线内陆城市新房每平米均价.gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '链家部分二线沿海城市新房每平米均价.gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '链家部分三线城市新房每平米均价.gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '链家部分四线城市新房每平米均价.gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '链家部分五线城市新房每平米均价.gif',
        ]
        return img_list

    # 每套房均价
    def avg_loupan_price(self, city):
        img_list = [
            self.img_base_path + sep + 'avg_loupan' + sep + '链家部分一线城市及新一线城市每套新房均价.gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '链家部分二线内陆城市每套新房均价.gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '链家部分二线沿海城市每套新房均价.gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '链家部分三线城市每套新房均价.gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '链家部分四线城市每套新房均价.gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '链家部分五线城市每套新房均价.gif',
        ]
        return img_list

    # 物业占比分布图
    def wuye_type_count(self, city):
        city_map = get_city_map('newhouse')
        data = []
        data.append(self.img_base_path + sep + 'wuye_type_count' + sep + '{}市新房物业类型占比分布图.gif'.format(city_map[city]))
        return data

    # 各户型占比
    def huxing_count(self, city):
        city_map = get_city_map('newhouse')
        data = []
        data.append(self.img_base_path + sep + 'huxing_count' + sep + '{}市新房户型占比分布图.gif'.format(city_map[city]))
        return data

    # 每平米最贵的top5楼盘
    def square_meter_max_top5(self, city):
        city_map = get_city_map('newhouse')
        data = []
        data.append(
            self.img_base_path + sep + 'square_meter_max_top5' + sep + '{}市新房每平米最贵top5楼盘.gif'.format(city_map[city]))
        return data

    # 每平米最便宜的top5楼盘
    def square_meter_min_top5(self, city):
        city_map = get_city_map('newhouse')
        data = []
        data.append(
            self.img_base_path + sep + 'square_meter_min_top5' + sep + '{}市新房每平米最便宜top5楼盘.gif'.format(city_map[city]))
        return data

    # 标签词云
    def tag_wordcloud(self, city):
        city_map = get_city_map('newhouse')
        data = []
        data.append(self.img_base_path + sep + 'tag_wordcloud' + sep + '{}市新房热门标签.gif'.format(city_map[city]))
        return data


class ershoufang_list():
    def __init__(self, city, analysis):
        data = []
        self.city = city
        self.analysis = analysis
        self.img_base_path = sep + 'static' + sep + 'ershoufang'
        self.result = {
            1: self.unit_price_range(city),
            2: self.total_price_range(city),
            3: self.avg_square_meter(city),
            4: self.avg_loupan_price(city),
            5: self.square_meter_max_top5(city),
            6: self.square_meter_min_top5(city),
            7: self.xiaoqu_wordcloud(city),
            8: self.position_wordcloud(city)
        }

    # 返回数据给前端
    def parse(self):
        return self.result[self.analysis]

    # 每平米价位占比
    def unit_price_range(self, city):
        city_map = get_city_map('ershoufang')
        print(city_map)
        data = []
        data.append(
            self.img_base_path + sep + 'unit_price_range' + sep + '{}市二手房每平米楼盘价位占比分布图.gif'.format(city_map[city]))
        print(self.img_base_path + sep + 'unit_price_range' + sep + '{}市二手房每平米楼盘价位占比分布图.gif'.format(city_map[city]))
        return data

    # 每套房各价位占比
    def total_price_range(self, city):
        city_map = get_city_map('ershoufang')
        data = []
        data.append(
            self.img_base_path + sep + 'total_price_range' + sep + '{}市二手房每套房价位占比分布图.gif'.format(city_map[city]))
        return data

    # 每平米均价
    def avg_square_meter(self, city):
        img_list = [
            self.img_base_path + sep + 'avg_square_meter' + sep + '一线城市二手房每平米均价.gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '新一线城市二手房每平米均价(1).gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '新一线城市二手房每平米均价(2).gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '二线城市二手房每平米均价(1).gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '二线城市二手房每平米均价(2).gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '二线城市二手房每平米均价(3).gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '三线城市二手房每平米均价(1).gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '三线城市二手房每平米均价(2).gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '三线城市二手房每平米均价(3).gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '四线城市二手房每平米均价(1).gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '四线城市二手房每平米均价(2).gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '四线城市二手房每平米均价(3).gif',
            self.img_base_path + sep + 'avg_square_meter' + sep + '五线城市二手房每平米均价.gif',
        ]
        return img_list

    # 每套房均价
    def avg_loupan_price(self, city):
        img_list = [
            self.img_base_path + sep + 'avg_loupan' + sep + '一线城市二手房每套均价.gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '新一线城市二手房每套均价(1).gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '新一线城市二手房每套均价(2).gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '二线城市二手房每套均价(1).gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '二线城市二手房每套均价(2).gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '二线城市二手房每套均价(3).gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '三线城市二手房每套均价(1).gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '三线城市二手房每套均价(2).gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '三线城市二手房每套均价(3).gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '四线城市二手房每套均价(1).gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '四线城市二手房每套均价(2).gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '四线城市二手房每套均价(3).gif',
            self.img_base_path + sep + 'avg_loupan' + sep + '五线城市二手房每套均价.gif',
        ]
        return img_list

    # 每平米最贵的top5楼盘
    def square_meter_max_top5(self, city):
        city_map = get_city_map('ershoufang')
        data = []
        data.append(
            self.img_base_path + sep + 'square_meter_max_top5' + sep + '{}市二手房每平米最贵top5小区.gif'.format(city_map[city]))
        return data

    # 每平米最便宜的top5楼盘
    def square_meter_min_top5(self, city):
        city_map = get_city_map('ershoufang')
        data = []
        data.append(
            self.img_base_path + sep + 'square_meter_min_top5' + sep + '{}市二手房每平米最便宜top5小区.gif'.format(city_map[city]))
        return data

    # 热门小区词云
    def xiaoqu_wordcloud(self, city):
        city_map = get_city_map('ershoufang')
        data = []
        data.append(self.img_base_path + sep + 'xiaoqu_wordcloud' + sep + '{}市二手房热门小区.gif'.format(city_map[city]))
        return data

    # 热门地段词云
    def position_wordcloud(self, city):
        city_map = get_city_map('ershoufang')
        data = []
        data.append(self.img_base_path + sep + 'position_wordcloud' + sep + '{}市二手房热门地段.gif'.format(city_map[city]))
        return data


class rent_list():
    def __init__(self, city, analysis):
        data = []
        self.city = city
        self.analysis = analysis
        self.img_base_path = sep + 'static' + sep + 'rent'
        self.result = {1: self.source_percentage(city),
                       2: self.brandtop5_avg_price(city),
                       3: self.avg_price_rent(city),
                       4: self.rent_max_top5(city),
                       5: self.rent_min_top5(city),
                       6: self.tag_wordcloud(city)
                       }

    # 返回数据给前端
    def parse(self):
        return self.result[self.analysis]

    #  每个品牌房源占比
    def source_percentage(self, city):
        city_map = get_city_map('rent')
        data = []
        data.append(self.img_base_path + sep + 'source_percentage' + sep + '{}市链家租房来源.gif'.format(city_map[city]))
        return data

    # 房源占比最高的top5均价
    def brandtop5_avg_price(self, city):
        city_map = get_city_map('rent')
        data = []
        data.append(self.img_base_path + sep + 'brand_avg_price' + sep + '{}市房源占比最高平台top5均价.gif'.format(city_map[city]))
        return data

    # 每平米均价
    def avg_price_rent(self, city):
        img_list = [
            self.img_base_path + sep + 'avg_price' + sep + '一线城市租房均价.gif',
            self.img_base_path + sep + 'avg_price' + sep + '新一线城市租房均价(1).gif',
            self.img_base_path + sep + 'avg_price' + sep + '新一线城市租房均价(2).gif',
            self.img_base_path + sep + 'avg_price' + sep + '二线城市租房均价(1).gif',
            self.img_base_path + sep + 'avg_price' + sep + '二线城市租房均价(2).gif',
            self.img_base_path + sep + 'avg_price' + sep + '二线城市租房均价(3).gif',
            self.img_base_path + sep + 'avg_price' + sep + '三线城市租房均价(1).gif',
            self.img_base_path + sep + 'avg_price' + sep + '三线城市租房均价(2).gif',
            self.img_base_path + sep + 'avg_price' + sep + '三线城市租房均价(3).gif',
            self.img_base_path + sep + 'avg_price' + sep + '四线城市租房均价(1).gif',
            self.img_base_path + sep + 'avg_price' + sep + '四线城市租房均价(2).gif',
            self.img_base_path + sep + 'avg_price' + sep + '四线城市租房均价(3).gif',
            self.img_base_path + sep + 'avg_price' + sep + '五线城市租房均价.gif',
        ]
        return img_list

    # 租房最贵top5
    def rent_max_top5(self, city):
        city_map = get_city_map('rent')
        data = []
        data.append(self.img_base_path + sep + 'rent_max_top5' + sep + '{}市租房价格最高top5.gif'.format(city_map[city]))
        return data

    # 租房最低top5
    def rent_min_top5(self, city):
        city_map = get_city_map('rent')
        data = []
        data.append(self.img_base_path + sep + 'rent_min_top5' + sep + '{}市租房价格最低top5.gif'.format(city_map[city]))
        return data

    # 租房标签词云
    def tag_wordcloud(self, city):
        city_map = get_city_map('rent')
        data = []
        data.append(self.img_base_path + sep + 'tag_wordcloud' + sep + '{}市租房热门标签.gif'.format(city_map[city]))
        return data
