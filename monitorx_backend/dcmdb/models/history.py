import json
from django.db import models
from dops.models import BaseModel
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet
from django.contrib.auth import get_user_model
User = get_user_model()


class History(BaseModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="操作人")
    model = models.CharField(max_length=255, verbose_name="模块", default="")
    action = models.CharField(max_length=255, verbose_name="动作")
    content = models.TextField(default=json.dumps([]), verbose_name="操作内容")


class HistorySerializer(serializers.ModelSerializer):
    user__username = serializers.CharField(source="user.username", read_only=True)
    user__first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = History
        fields = "__all__"


class HistoryFilter(FilterSet):
    class Meta:
        model = History
        fields = {
            "id": ["exact", "in"],
        }


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all().order_by("id")
    filter_class = HistoryFilter
    serializer_class = HistorySerializer
