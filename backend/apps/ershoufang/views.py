# Create your views here.
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ershoufang.serializers import ErShouFangSerializer
from ershoufang.models import ErShouFang


class ErShouFangView(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ErShouFangSerializer
    queryset = ErShouFang.objects.all()

    def list(self, request):
        queryset = ErShouFang.objects.all()
        serializer = ErShouFang(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super(ErShouFangView, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
