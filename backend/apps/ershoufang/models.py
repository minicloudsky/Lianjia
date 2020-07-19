from django.db import models

from utils.model import BaseModel
from django_mysql.models import JSONField


# Create your models here.
class ErShouFang(BaseModel):
    house_url = models.CharField('房源url', max_length=500, null=False, blank=False)
    city = models.CharField('房源所在城市', max_length=100, null=True, blank=True)
    name = models.CharField('房源名称', max_length=500, null=True, blank=True)
    total_price = models.FloatField('总价', default=0)
    unit_type = models.CharField('房型', max_length=200, null=True, blank=True)
    square = models.FloatField('面积', default=0)
    #
    detail = JSONField()
    unit_price = models.FloatField('单价', default=0)
    upload_time = models.DateTimeField('房源挂牌时间', blank=True, null=True)
    orientation = models.CharField('朝向', max_length=100, null=True, blank=True)
    floor = models.CharField('楼层', max_length=100, null=True, blank=True)
    building_type = models.CharField('房屋类型', max_length=100, null=True, blank=True)
    elevator = models.CharField('电梯', max_length=100, null=True, blank=True)
    renovation = models.CharField('装修', max_length=100, null=True, blank=True)
    purpose = models.CharField('用途', max_length=100, null=True, blank=True)
    ownership = models.CharField('权属', max_length=100, null=True, blank=True)
    down_payment_budget = models.CharField('首付预算', max_length=100, null=True, blank=True)
    community = models.CharField('小区', max_length=100, null=True, blank=True)
    # 房间信息
    room_info = JSONField()
    introduction = models.TextField('房源介绍')
    trends = models.TextField('房源趋势')
    basic_attributes = models.TextField('基础属性')
    position = models.CharField('位置', max_length=300, null=True, blank=True)
    highlight = models.TextField('房源亮点')
    img_url = models.CharField('房源图片', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
