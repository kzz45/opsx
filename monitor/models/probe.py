from django.db import models
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers


class Probe(BaseModel):
    class Meta:
        verbose_name_plural = "探测节点"

    name = models.CharField(max_length=255, verbose_name="节点名称")
    desc = models.TextField(verbose_name="描述", default="")
    api = models.CharField(max_length=255, verbose_name="对外API地址", default="")
    ipaddr = models.CharField(max_length=255, verbose_name="IP地址", default="")
    uuid = models.CharField(max_length=255, verbose_name="唯一ID", blank=True)
    mode = models.CharField(max_length=255, verbose_name="探测模式", default="http")  # tcp/http/ping/snmp

    def __str__(self):
        return self.name


class ProbeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Probe
        fields = "__all__"


class ProbeFilter(FilterSet):
    class Meta:
        model = Probe
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class ProbeViewSet(viewsets.ModelViewSet):
    queryset = Probe.objects.all().order_by("id")
    filter_class = ProbeFilter
    serializer_class = ProbeSerializer
