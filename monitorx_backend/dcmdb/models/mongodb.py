from django.db import models
from dops.models import BaseModel
from dcmdb.models.project import Project
from dcmdb.models.factory import Factory
from dcmdb.models.region import Region
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Mongodb(BaseModel):
    mongodb_status_choices = ((0, "空闲中"), (1, "使用中"), (2, "已退还"), (3, "待退还"))

    external_name = models.CharField(max_length=255, verbose_name="外部名称", null=True)
    external_uuid = models.CharField(max_length=255, verbose_name="外部ID", unique=True)
    status = models.IntegerField(verbose_name="状态", choices=mongodb_status_choices, default=0)
    db_type = models.CharField(max_length=255, verbose_name="实例类型", default="replicate")
    replica_set_name = models.CharField(max_length=255, verbose_name="副本集名称", null=True, blank=True)
    disk = models.IntegerField(default=0, verbose_name="磁盘")
    iops = models.IntegerField(default=0, verbose_name="IOPS")
    connections = models.IntegerField(default=0, verbose_name="Connections")
    version = models.CharField(max_length=255, verbose_name="版本", null=True, blank=True)
    flavor_name = models.CharField(max_length=255, verbose_name="机型", null=True, blank=True)
    primary_conn = models.CharField(max_length=255, verbose_name="连接地址", null=True, blank=True)
    primary_port = models.IntegerField(default=3717, verbose_name="连接端口")
    secondary_conn = models.CharField(max_length=255, verbose_name="连接地址", null=True, blank=True)
    secondary_port = models.IntegerField(default=3717, verbose_name="连接端口")
    readonly_conn = models.CharField(max_length=255, verbose_name="连接地址", null=True, blank=True)
    readonly_port = models.IntegerField(default=3717, verbose_name="连接端口")
    shard_conn = models.CharField(max_length=255, verbose_name="", null=True, blank=True)
    mongos_conn = models.CharField(max_length=255, verbose_name="", null=True, blank=True)
    mongos_port = models.IntegerField(default=3717, verbose_name="")
    region = models.ForeignKey(to=Region, on_delete=models.CASCADE, verbose_name="所属地区", null=True, blank=True)
    factory = models.ForeignKey(to=Factory, on_delete=models.CASCADE, verbose_name="厂商", null=True, blank=True)
    project = models.ForeignKey(to=Project, related_name="mongodb_list", on_delete=models.CASCADE, verbose_name="项目", null=True, blank=True)

    def __str__(self):
        return self.external_uuid


class MongodbSerializer(serializers.ModelSerializer):
    region__name = serializers.CharField(source="region.name", read_only=True)
    factory__name = serializers.CharField(source="factory.name", read_only=True)
    class Meta:
        model = Mongodb
        fields = "__all__"


class MongodbFilter(FilterSet):
    class Meta:
        model = Mongodb
        fields = {
            "id": ["exact", "in"],
            "status": ["exact", "in"],
            "external_name": ["exact", "in", "contains"],
            "external_uuid": ["exact", "in", "contains"],
            "db_type": ["exact", "in", "contains"],
            "region__name": ["exact", "in", "contains"],
            "factory__name": ["exact", "in", "contains", "startswith"],
            "project__id": ["exact", "in", "isnull"],
            "project__product__id": ["exact", "in"],
            "project__product__name": ["exact", "in", "contains"],
        }


class MongodbViewSet(viewsets.ModelViewSet):
    queryset = Mongodb.objects.all().order_by("-id")
    filter_class = MongodbFilter
    serializer_class = MongodbSerializer
