import json
from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from dmonitor.models.probe import Probe
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class ProbeTask(BaseModel):
    name = models.CharField(max_length=255, verbose_name="探测任务名称")
    mode = models.CharField(max_length=36, verbose_name="探测类型")  # http,tcp,ping
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, blank=True)
    group = models.CharField(max_length=255, verbose_name="探测任务分组", null=True)
    interval = models.IntegerField(default=60, verbose_name="间隔时间")
    timeout = models.IntegerField(default=30, verbose_name="超时时间")
    target = models.CharField(max_length=255, verbose_name="目标")
    probe = models.ManyToManyField(to=Probe, verbose_name="探测")
    label = models.TextField(default=json.dumps([]), verbose_name="标签", blank=True)

    def __str__(self):
        return self.name


class ProbeTaskSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = ProbeTask
        fields = "__all__"


class ProbeTaskFilter(FilterSet):
    class Meta:
        model = ProbeTask
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class ProbeTaskViewSet(viewsets.ModelViewSet):
    queryset = ProbeTask.objects.all().order_by("id")
    filter_class = ProbeTaskFilter
    serializer_class = ProbeTaskSerializer
