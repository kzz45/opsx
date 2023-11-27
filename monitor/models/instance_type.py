from django.db import models
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers


class InstanceType(BaseModel):
    class Meta:
        verbose_name_plural = "对象类型"

    name = models.CharField(max_length=255, verbose_name="名称")
    desc = models.CharField(max_length=255, verbose_name="别名", null=True)

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
