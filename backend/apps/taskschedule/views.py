# Create your views here.
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from taskschedule.serializers import TaskScheduleSerializer
from taskschedule.models import Task
from taskschedule.tasks import crawl_ershoufang


class TaskScheduleView(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = []
    serializer_class = TaskScheduleSerializer
    queryset = Task.objects.all()

    def list(self, request):
        queryset = Task.objects.all()
        serializer = TaskScheduleSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        crawl = crawl_ershoufang()
        return Response(data={'code': 1, 'msg': '二手房爬虫创建成功'}, status=status)
        # return super(TaskScheduleView, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
