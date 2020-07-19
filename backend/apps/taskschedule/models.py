from django.db import models
from model import BaseModel


# Create your models here.
class Task(BaseModel):
    start_time = models.DateTimeField('任务开始时间')
    end_time = models.DateTimeField('任务结束时间')
