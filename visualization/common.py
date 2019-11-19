import time
import pymongo
import os
from lianjia.constants import *
from config.configs import *

base_path = web_static_base_path
# 字符串模板
main_price_range_template = '{}市新房每平米楼盘价位占比分布图'
second_price_range_template = '{}市每套新房价位占比分布图'
avg_price_square_meter = '链家各城市新房每平米价格'
temproary_loss = '0为该城市暂无数据'
# 每平米均价模板
first_level_avg_square_template = '链家部分一线城市及新一线城市新房每平米均价'
second_level_land_avg_square_template = '链家部分二线内陆城市新房每平米均价'
second_level_sea_avg_square_template = '链家部分二线沿海城市新房每平米均价'
third_level_avg_square_template = '链家部分三线城市新房每平米均价'
forth_level_avg_square_template = '链家部分四线城市新房每平米均价'
fifth_level_avg_square_template = '链家部分五线城市新房每平米均价'
# 每套均价模板
first_level_avg_loupan = '链家部分一线城市及新一线城市每套新房均价'
second_level_land_avg_loupan = '链家部分二线内陆城市每套新房均价'
second_level_sea_avg_loupan = '链家部分二线沿海城市每套新房均价'
third_level_avg_loupan = '链家部分三线城市每套新房均价'
forth_level_avg_loupan = '链家部分四线城市每套新房均价'
fifth_level_avg_loupan = '链家部分五线城市每套新房均价'
# 物业类型占比分布图
wuye_type_count_template = '{}市新房物业类型占比分布图'
# 户型占比分布图
huxing_count_template = '{}市新房户型占比分布图'
#
square_price_max_top5 = '{}市新房每平米最贵top5楼盘'
square_price_min_top5 = '{}市新房每平米最便宜top5楼盘'
tag_wordcloud_template = '{}市楼盘标签词云图'
# 每平米最高统计400000每平米的房价
max_main_price = 200000
# 每套房统计最高统计9000万的价格
max_second_price = 90000
img_name = '{}' + sep + '{}.gif'
# 链家中国新房城市划分
first_level = ['天津', '青岛', '上海', '郑州', '南京', '沈阳', '重庆', '广州',
               '武汉', '深圳', '长沙', '大连', '成都', '西安', '杭州', '苏州', '东莞', ]
second_land_level = ['长春', '南昌', '无锡', '石家庄', '呼和浩特', '太原', '昆明', '合肥', '绍兴',
                     '贵阳', '济南', ]
second_near_sea_level = [
    '佛山', '惠州', '嘉兴', '中山', '烟台', '徐州', '厦门', '海口', '南通', '泉州', '珠海'
]
third_level = ['镇江', '保定', '威海', '清远', '廊坊', '秦皇岛', '漳州', '湖州', '三亚', ]
forth_level = ['承德', '邢台', '大理', '晋中', '滁州', '西双版纳', '张家口', ]
fifth_level = ['保亭', '黄冈', '陵水', '儋州', '乐东', '琼海', '万宁',
               '定安', '临高', '文昌', '澄迈', '琼中', '五指山', ]
# 链家二手房城市划分
lianjia_citys = {}
lianjia_citys['first'] = ['北京', '深圳', '广州', '上海', ]
lianjia_citys['new_first'] = ['长沙', '苏州', '青岛', '武汉', '大连', '天津', '沈阳',
                              '郑州', '成都', '杭州', '宁波', '东莞', '南京', '西安', '重庆', ]
lianjia_citys['second'] = ['长春', '常州', '台州', '南宁', '合肥', '珠海', '无锡', '石家庄',
                           '昆明', '贵阳', '金华', '哈尔滨', '中山', '嘉兴', '太原', '温州',
                           '海口', '泉州', '惠州', '厦门', '兰州', '福州', '南通', '佛山', '济南',
                           '烟台', '绍兴', '南昌', ]
lianjia_citys['third'] = ['九江', '南充', '盐城', '岳阳', '保定', '清远', '上饶', '襄阳', '丹东',
                          '江门', '龙岩', '秦皇岛', '镇江', '柳州', '威海', '洛阳', '湛江', '马鞍山',
                          '芜湖', '廊坊', '湖州', '淮安', '绵阳', '宜昌', '漳州', '桂林', '株洲',
                          '银川', '临沂', '淄博', '呼和浩特', '赣州', '昆山', '三亚', '唐山', '潍坊', ]
lianjia_citys['forth'] = ['承德', '大理', '滁州', '许昌', '眉山', '咸宁', '常德', '张家口',
                          '开封', '黄石', '德阳', '黄冈', '新乡', '晋中', '西双版纳', '吉安',
                          '安庆', '乐山', '邢台', '咸阳', '吉林', '宝鸡', '北海', ]
lianjia_citys['fifth'] = ['凉山', '达州', '汉中', '临高', '保亭', '五指山', ]


# 生成每平米价格的范围过滤条件
def gen_match(price, delta):
    price_range_map = {}
    for i in range(0, price, delta):
        price_range_map['{}-{}'.format(i, i + delta)] = {
            '$gte': i,
            '$lt': i + delta
        }
    return price_range_map


# 获取main_price各区间分布
def get_main_price_range(city):
    client = pymongo.MongoClient()
    db = 'lianjia_newhouse' + str(time.strftime('%Y%m%d', time.localtime(time.time())))
    db = client[db]
    collection = db[city]
    price = max_main_price
    while price > 1000:
        result = list(collection.find({'main_price': {'$gte': price}}))
        if result and len(result) > 5:
            if price > 100000:
                return gen_match(price, 20000)
            if price > 50000:
                return gen_match(price, 10000)
            if price > 30000:
                return gen_match(price, 5000)
            return gen_match(price, 3000)
        else:
            price = int(price / 2)


# 获取second_price各区间分布
def get_second_price_range(city):
    client = pymongo.MongoClient()
    db = 'lianjia_newhouse' + str(time.strftime('%Y%m%d', time.localtime(time.time())))
    db = client[db]
    collection = db[city]
    price = max_second_price
    while price > 10:
        result = list(collection.find({'second_price': {'$gte': price}}))
        # 极少数价格区间去掉
        if result and len(result) > 5:
            if price > 5000:
                return gen_match(price, 1000)
            if price > 3000:
                return gen_match(price, 400)
            if price > 1000:
                return gen_match(price, 200)
            if price > 500:
                return gen_match(price, 70)
            if price > 200:
                return gen_match(price, 30)
            return gen_match(price, 15)
        price = int(price / 2)


# 获取unit_price各区间分布
def get_unit_price_range(city):
    client = pymongo.MongoClient()
    db = 'lianjia_ershoufang' + str(time.strftime('%Y%m%d', time.localtime(time.time())))
    db = client[db]
    collection = db[city]
    price = max_main_price
    while price > 1000:
        result = list(collection.find({'unit_price': {'$gte': price}}))
        if result and len(result) > 5:
            if price > 100000:
                return gen_match(price, 15000)
            if price > 50000:
                return gen_match(price, 7000)
            if price > 30000:
                return gen_match(price, 5000)
            return gen_match(price, 3000)
        else:
            price = int(price / 2)


# 获取total_price各区间分布
def get_total_price_range(city):
    client = pymongo.MongoClient()
    db = 'lianjia_ershoufang' + str(time.strftime('%Y%m%d', time.localtime(time.time())))
    db = client[db]
    collection = db[city]
    price = max_second_price
    while price > 10:
        result = list(collection.find({'total_price': {'$gte': price}}))
        if result and len(result) > 5:
            if price > 5000:
                return gen_match(price, 1000)
            if price > 3000:
                return gen_match(price, 400)
            if price > 1000:
                return gen_match(price, 200)
            if price > 500:
                return gen_match(price, 70)
            if price > 200:
                return gen_match(price, 30)
            return gen_match(price, 15)
        price = int(price / 2)
