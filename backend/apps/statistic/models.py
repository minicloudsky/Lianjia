from django.db import models
from backend.utils.model import BaseModel


# Create your models here.
# 数据统计
class Statistic(BaseModel):
    start_time = models.DateTimeField('爬虫开始时间')
    end_time = models.DateTimeField('爬虫结束时间')
    total = models.IntegerField('房源总数', default=0)
    city = models.CharField('城市', max_length=100, default='')
    house_types = (
        ('ershoufang', '二手房'),
        ('newhouse', '新房'),
        ('zufang', '租房'),
    )
    type = models.CharField('房源类型', choices=house_types, default='ershoufang', max_length=50)
    cost_time = models.CharField('耗时', max_length=100,default='')

    def __str__(self):
        return self.city_url + "_" + str(self.start_time)
