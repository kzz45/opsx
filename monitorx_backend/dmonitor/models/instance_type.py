# 实例类型：机器、域名等

from django.db import models
from dmonitor.models.base import BaseModel
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class InstanceType(BaseModel):
    name = models.CharField(max_length=255, verbose_name="实例类型名称")  # machine switch domain
    value = models.CharField(max_length=255, verbose_name="实体类型", null=True)

    def __str__(self):
        return self.name


class InstanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstanceType
        fields = "__all__"


class InstanceTypeFilter(FilterSet):
    class Meta:
        model = InstanceType
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class InstanceTypeViewSet(viewsets.ModelViewSet):
    queryset = InstanceType.objects.all().order_by("id")
    filter_class = InstanceTypeFilter
    serializer_class = InstanceTypeSerializer
