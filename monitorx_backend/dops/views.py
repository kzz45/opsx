import os
import jwt
import json
import time
import urllib
import hashlib
import datetime
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model


class BasicLogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        User = get_user_model()
        user = User.objects.filter(username=username).filter(
            password=password).first()
        if not user:
            msg = {
                "msg": "login failed: user not exists",
                "token": None
            }
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)
        else:
            token = jwt.encode({
                "username": username,
                "password": password,
                "timestamp": str(int(time.time())),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=86400)
            },
                settings.SECRET_KEY,
                algorithm="HS256"
            )
            user.token = token
            user.save()
            msg = {
                "msg": "login success",
                "user_id": user.id,
                "username": user.username,
                "token": token
            }
        return Response(data=msg, status=status.HTTP_200_OK)


class BasicLouout(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
