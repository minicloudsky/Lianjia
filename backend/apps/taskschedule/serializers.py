from rest_framework.serializers import ModelSerializer
from taskschedule.models import Task


class TaskScheduleSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
