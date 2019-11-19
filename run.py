from visualization.data_analysis import data_analysis
from spider.crawl_lianjia import crawl_lianjia
from lianjia.app import app
import time
from config.configs import *

if __name__ == '__main__':
    init_time = int(time.time())
    spider = crawl_lianjia()
    data = data_analysis()
    web = app.run()