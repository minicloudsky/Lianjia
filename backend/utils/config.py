import redis
import logging

logger = logging.getLogger("lianjia")
redis_url = 'aliyun.yawujia.cn'
cache_one_day = 86400
mysql_user = 'root'
mysql_password = 'root'
city_default_max_page = 500

city_dict_key = 'city_dict_v1'
ershoufang_city_house_urls_key = 'ershoufang_city_house_urls_v1'


def get_redis_conn():
    redis_conn = redis.Redis(redis_url)
    return redis_conn
