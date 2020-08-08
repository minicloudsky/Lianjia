from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class BaseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        data = {"code": 200, "data": {}}
        return Response(status=status.HTTP_200_OK, data=data)

    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(status=status.HTTP_200_OK, data=data)
