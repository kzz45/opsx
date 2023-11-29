import time
from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


def get_current_ts():
    return int(time.time())


class Alert(BaseModel):
    name = models.CharField(max_length=255, verbose_name="告警名称")
    instance_type = models.CharField(max_length=255, verbose_name="实例类型", null=True)
    instance_name = models.CharField(max_length=255, default='-', verbose_name="实例名称")
    ipaddr = models.CharField(max_length=255, verbose_name="IP地址", null=True)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品", null=True)
    endpoint = models.CharField(max_length=255, verbose_name="端点")
    level = models.CharField(max_length=255, verbose_name="级别")
    state = models.CharField(max_length=255, verbose_name="状态")
    labels = models.TextField(verbose_name="标签", null=True)
    graph = models.TextField(verbose_name="图", null=True)
    summary = models.TextField(default='', blank=True, verbose_name="消息")
    description = models.TextField(default='', blank=True, verbose_name="描述")
    start = models.IntegerField(verbose_name="开始时间", default=0)
    end = models.IntegerField(verbose_name="结束时间", default=0)
    receivers = models.TextField(verbose_name="接收人", null=True)
    # create_at = models.IntegerField(default=get_current_ts, verbose_name="发生时间")

    def __str__(self):
        return self.name


class AlertSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Alert
        fields = "__all__"


class AlertFilter(FilterSet):
    class Meta:
        model = Alert
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "state": ["exact", "in", "contains"],
            "endpoint": ["exact", "in", "contains"],
            "product__id": ["exact", "in"],
            "product__name": ["exact", "in", "contains"],
        }


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all().order_by("-start")
    filter_class = AlertFilter
    serializer_class = AlertSerializer
