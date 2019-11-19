from django.db import models


# Create your models here.
class NewHouse(models.Model):
    loupan = models.CharField(verbose_name='楼盘', max_length=1000)
    city = models.CharField(verbose_name='城市', max_length=100)
    loupan_url = models.CharField(verbose_name='楼盘链接', max_length=2000)
    wuye_type = models.CharField(verbose_name='物业类型', max_length=2000)
    sale_status = models.IntegerField(verbose_name='销售状态')
    img_url = models.CharField(verbose_name='楼盘图片链接', max_length=2000)
    location = models.CharField(verbose_name='位置', max_length=1000)
    huxing = models.CharField(verbose_name='户型', max_length=1000)
    area = models.CharField(verbose_name='面积')


class SecondHandHouse(models.Model):
    loupan = models.CharField(verbose_name='楼盘')


class RentHouse(models.Model):
    loupan = models.CharField(verbose_name='楼盘')
