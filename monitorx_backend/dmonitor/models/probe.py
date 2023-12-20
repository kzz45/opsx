# 探测节点

from django.db import models
from dmonitor.models.base import BaseModel
from dmonitor.models.server_group import ServerGroup
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Probe(BaseModel):
    name = models.CharField(max_length=255, verbose_name="探测名称")
    desc = models.TextField(verbose_name="描述", null=True, blank=True)
    api = models.CharField(max_length=255, verbose_name="对外API地址")
    ipaddr = models.CharField(max_length=255, verbose_name="IP地址")
    uuid = models.CharField(max_length=255, verbose_name="唯一ID", blank=True)
    mode = models.CharField(max_length=255, verbose_name="探测模式")  # tcp/http/ping/snmp
    server_group = models.ForeignKey(to=ServerGroup, on_delete=models.PROTECT, verbose_name="关联采集组", default=None, blank=True)

    def __str__(self):
        return self.name


class ProbeSerializer(serializers.ModelSerializer):
    server_group__name = serializers.CharField(source="server_group.name", read_only=True)

    class Meta:
        model = Probe
        fields = "__all__"


class ProbeFilter(FilterSet):
    class Meta:
        model = Probe
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "server_group__id": ["exact", "in"],
            "server_group__name": ["exact", "in", "contains"],
        }


class ProbeViewSet(viewsets.ModelViewSet):
    queryset = Probe.objects.all().order_by("id")
    filter_class = ProbeFilter
    serializer_class = ProbeSerializer
