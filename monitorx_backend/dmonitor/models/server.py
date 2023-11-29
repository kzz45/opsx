# Prometheus服务器

from django.db import models
from dmonitor.models.base import BaseModel
from dmonitor.models.server_group import ServerGroup
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Server(BaseModel):
    name = models.CharField(max_length=255, verbose_name="名称")
    desc = models.TextField(verbose_name="描述", null=True, default=None)
    code = models.CharField(max_length=255, verbose_name="服务唯一标识")
    uuid = models.CharField(max_length=255, verbose_name="唯一ID", blank=True)
    ipaddr = models.CharField(max_length=255, verbose_name="IP地址")
    server_group = models.ForeignKey(to=ServerGroup, on_delete=models.PROTECT, verbose_name="服务器组", null=True)

    def __str__(self):
        return self.name


class ServerSerializer(serializers.ModelSerializer):
    server_group__id = serializers.IntegerField(source="server_group.id", read_only=True)
    server_group__name = serializers.CharField(source="server_group.name", read_only=True)

    class Meta:
        model = Server
        fields = "__all__"


class ServerFilter(FilterSet):
    class Meta:
        model = Server
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "uuid": ["exact", "in", "contains"],
            "ipaddr": ["exact", "in", "contains"],
            "server_group__id": ["exact", "in", "contains"],
        }


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all().order_by("id")
    filter_class = ServerFilter
    serializer_class = ServerSerializer
