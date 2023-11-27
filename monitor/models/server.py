from django.db import models
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers


class Server(BaseModel):
    class Meta:
        verbose_name_plural = "采集节点"

    name = models.CharField(max_length=255, verbose_name="节点名称")
    desc = models.CharField(max_length=255, verbose_name="", null=True)
    code = models.CharField(max_length=255, verbose_name="唯一标识")
    uuid = models.CharField(max_length=255, verbose_name="唯一ID")
    ipaddr = models.CharField(max_length=255, verbose_name="IP地址")
    port = models.IntegerField(verbose_name="监听端口", default=9090)
    alertmanager = models.CharField(max_length=255, verbose_name="Alertmanager地址", null=True)
    unit = models.CharField(max_length=255, verbose_name="存储时间单位", default="d")
    retention_time = models.IntegerField(verbose_name="存储时间", default=15)
    retention_size = models.IntegerField(verbose_name="存储块大小", default=512)
    query_timeout = models.IntegerField(verbose_name="查询超时", default=2)
    query_concurrency = models.IntegerField(verbose_name="查询并发", default=20)

    def __str__(self):
        return self.name


class ServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Server
        fields = "__all__"


class ServerFilter(FilterSet):
    class Meta:
        model = Server
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "desc": ["exact", "in", "contains"],
            "code": ["exact", "in", "contains"],
            "uuid": ["exact", "in", "contains"],
            "ipaddr": ["exact", "in", "contains"],
        }


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all().order_by("id")
    filter_class = ServerFilter
    serializer_class = ServerSerializer

    # 只有管理员可以添加
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # 只有管理员可以更新
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
