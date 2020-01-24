from django.db import models


# Create your models here.
class ErshouFang():
    name = models.CharField(max_length=255, blank=True, null=True)
    detail_url = models.TextField()
    total_price = models.PositiveIntegerField('总价', default=0)
    unit_price = models.PositiveIntegerField('每平米价格', default=0)
    img_url = models.TextField()

