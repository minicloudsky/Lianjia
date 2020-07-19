from rest_framework.serializers import ModelSerializer
from ershoufang.models import ErShouFang


class ErShouFangSerializer(ModelSerializer):
    class Meta:
        model = ErShouFang
        fields = "__all__"
