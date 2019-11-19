# coding=utf-8
# 一天更新一次数据，爬取一次数据最少需4个小时，因此数据更新时间应该大于4小时
import os
import time

data_update_frequency = 3600 * 24
spider_status = ''
data_analysis_status = ''
data_update_time = ''
sep = os.sep


# return the newhouse database name
def newhousedb():
    return 'lianjia_newhouse' + str(time.strftime('%Y%m%d', time.localtime(time.time())))


# return the ershoufang database name
def ershoufangdb():
    return 'lianjia_ershoufang' + str(time.strftime('%Y%m%d', time.localtime(time.time())))


# return the rent house database name
def rentdb():
    return 'lianjia_rent' + str(time.strftime('%Y%m%d', time.localtime(time.time())))
