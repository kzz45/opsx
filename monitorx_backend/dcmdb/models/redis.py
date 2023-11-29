from django.db import models
from dcmdb.models.region import Region
from dops.models import BaseModel
from dcmdb.models.project import Project
from dcmdb.models.factory import Factory
from dcmdb.models.subnet import Subnet
from dcmdb.models.tag import Tag
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Redis(BaseModel):
    class Meta:
        verbose_name_plural = "Redis"

    redis_status_choices = ((0, "空闲中"), (1, "使用中"), (2, "已退还"), (3, "待退还"))
    redis_type_choices = ((0, "集群版"), (1, "标准版"))

    external_name = models.CharField(max_length=255, verbose_name="外部名称", null=True)
    external_uuid = models.CharField(max_length=255, verbose_name="外部ID", unique=True)
    status = models.IntegerField(verbose_name="状态", choices=redis_status_choices, default=0)
    available = models.BooleanField(default=False, verbose_name="是否可用")
    types = models.IntegerField(verbose_name="redis类型", choices=redis_type_choices, default=0)
    conn = models.CharField(max_length=255, verbose_name="连接地址", blank=True)
    port = models.IntegerField(default=3306, verbose_name="连接端口", blank=True)
    private_ip = models.CharField(max_length=255, verbose_name="内网地址", null=True, blank=True)
    public_ip = models.CharField(max_length=255, verbose_name="外网地址", null=True, blank=True)
    capacity = models.IntegerField(default=0, verbose_name="容量")
    qps = models.IntegerField(default=0, verbose_name="QPS")
    subnet = models.ForeignKey(to=Subnet, on_delete=models.CASCADE, verbose_name="子网", null=True, blank=True)
    factory = models.ForeignKey(to=Factory, on_delete=models.CASCADE, verbose_name="厂商", null=True, blank=True)
    project = models.ForeignKey(to=Project, related_name="redis_list", on_delete=models.CASCADE, verbose_name="项目", null=True, blank=True)
    tags = models.ManyToManyField(to=Tag, related_name="redis_tags", verbose_name="标签", blank=True)

    def __str__(self):
        return self.external_uuid


class RedisSerializer(serializers.ModelSerializer):
    # region__name = serializers.CharField(source="region.name", read_only=True)
    subnet__name = serializers.CharField(source="subnet_name", read_only=True)
    factory__name = serializers.CharField(source="factory.name", read_only=True)
    project__name = serializers.CharField(source="project.name", read_only=True)

    class Meta:
        model = Redis
        fields = "__all__"


class RedisFilter(FilterSet):
    class Meta:
        model = Redis
        fields = {
            "id": ["exact", "in"],
            "external_name": ["exact", "in", "contains"],
            "external_uuid": ["exact", "in", "contains"],
            "status": ["exact", "in"],
            "private_ip": ["exact", "in", "contains"],
            "project__id": ["exact", "in", "isnull"],
            # "region__name": ["exact", "in", "contains"],
            "factory__name": ["exact", "in", "contains", "startswith"],
            "project__name": ["exact", "in", "contains"],
            "project__product__id": ["exact", "in"],
            "project__product__name": ["exact", "in", "contains"],
        }


class RedisViewSet(viewsets.ModelViewSet):
    queryset = Redis.objects.all().order_by("-id")
    filter_class = RedisFilter
    serializer_class = RedisSerializer
