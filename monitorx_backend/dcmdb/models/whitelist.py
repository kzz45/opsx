# 公司出口IP白名单

from django.db import models
from dops.models import BaseModel
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class WhiteList(BaseModel):
    name = models.CharField(max_length=255, verbose_name="名称")
    desc = models.CharField(max_length=255, verbose_name="描述")
    ipaddr = models.CharField(max_length=255, verbose_name="IP地址")

    def __str__(self):
        return self.name


class WhiteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhiteList
        fields = "__all__"


class WhiteListFilter(FilterSet):
    class Meta:
        model = WhiteList
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class WhiteListViewSet(viewsets.ModelViewSet):
    queryset = WhiteList.objects.all().order_by("id")
    filter_class = WhiteListFilter
    serializer_class = WhiteListSerializer