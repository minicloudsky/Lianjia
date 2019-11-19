from visualization.newhouse import newhouse
from visualization.ershoufang import ershoufang
from visualization.rent import rent
import os
from config.configs import *


def data_analysis():
    print('start data analysis')
    print(os.getcwd())
    os.chdir('visualization')
    print(os.getcwd())
    data_analysis_status = '正在进行二手房数据分析'
    one = ershoufang()
    data_analysis_status = '正在进行新房数据分析'
    two = newhouse()
    data_analysis_status = '正在进行租房数据分析'
    three = rent()
    os.chdir(os.pardir)
    print(os.getcwd())
