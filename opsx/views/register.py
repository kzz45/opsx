from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User


class Register(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        user_obj = User(
            username=username,
            password=password,
        )
        user_obj.save()
        return Response(data=None, status=status.HTTP_201_CREATED)
