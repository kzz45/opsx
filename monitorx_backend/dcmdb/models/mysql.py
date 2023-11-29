from django.db import models
from dcmdb.models.region import Region
from dops.models import BaseModel
from dcmdb.models.project import Project
from dcmdb.models.factory import Factory
from dcmdb.models.subnet import Subnet
from dcmdb.models.tag import Tag
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class MySQL(BaseModel):
    class Meta:
        verbose_name_plural = "MySQL"

    mysql_status_choices = ((0, "空闲中"), (1, "使用中"), (2, "已退还"), (3, "待退还"))

    external_name = models.CharField(max_length=255, verbose_name="名称", null=True, blank=True)
    external_uuid = models.CharField(max_length=255, verbose_name="外部ID", unique=True)
    external_status = models.CharField(max_length=255, verbose_name="状态", null=True, blank=True)
    local_status = models.IntegerField(verbose_name="状态", choices=mysql_status_choices, default=0)
    conn = models.CharField(max_length=255, verbose_name="连接地址", null=True, blank=True)
    port = models.IntegerField(default=3306, verbose_name="连接端口", null=True)
    cpu = models.IntegerField(default=0, verbose_name="CPU")
    mem = models.IntegerField(default=0, verbose_name="内存")
    disk = models.IntegerField(default=0, verbose_name="磁盘")
    iops = models.IntegerField(default=0, verbose_name="IOPS")
    version = models.CharField(max_length=255, verbose_name="版本", null=True, blank=True)
    flavor_name = models.CharField(max_length=255, verbose_name="机型", null=True, blank=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)
    region = models.ForeignKey(to=Region, on_delete=models.CASCADE, verbose_name="地区", null=True, blank=True)
    subnet = models.ForeignKey(to=Subnet, on_delete=models.CASCADE, verbose_name="子网", null=True, blank=True)
    factory = models.ForeignKey(to=Factory, on_delete=models.CASCADE, verbose_name="厂商", null=True, blank=True)
    project = models.ManyToManyField(to=Project, related_name="mysql_list", verbose_name="项目", blank=True)
    tags = models.ManyToManyField(to=Tag, related_name="mysql_tags", verbose_name="标签", blank=True)

    def __str__(self):
        return self.external_uuid


class MySQLSerializer(serializers.ModelSerializer):
    region__name = serializers.CharField(source="region.name", read_only=True)
    factory__name = serializers.CharField(source="factory.name", read_only=True)
    # project_ids = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), many=True, read_only=False, source="project")

    class Meta:
        model = MySQL
        fields = "__all__"


class MySQLFilter(FilterSet):
    class Meta:
        model = MySQL
        fields = {
            "id": ["exact", "in"],
            "external_name": ["exact", "in", "contains"],
            "external_uuid": ["exact", "in", "contains"],
            "conn": ["exact", "in", "contains"],
            "factory__name": ["exact", "in", "contains", "startswith"],
            "project__id": ["exact", "in", "isnull"],
            "project__product__id": ["exact", "in"],
            "project__product__name": ["exact", "in", "contains"],
            "local_status": ["exact", "in"],
        }


class MySQLViewSet(viewsets.ModelViewSet):
    queryset = MySQL.objects.all().order_by("-id")
    filter_class = MySQLFilter
    serializer_class = MySQLSerializer
