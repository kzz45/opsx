# 监控对象实例 可以是机器 可以是域名 可以是交换机等

from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from dmonitor.models.label import Label, LabelSerializer
from dmonitor.models.server_group import ServerGroup
from dmonitor.models.instance_type import InstanceType
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Instance(BaseModel):
    name = models.CharField(max_length=255, verbose_name="实例名称(hostname)")
    endpoint = models.CharField(max_length=255, verbose_name="endpoint(机器唯一ID)", unique=True)
    private_ip = models.CharField(max_length=255, verbose_name="内网IP地址", null=True, blank=True)  # 默认内网IP地址
    public_ip = models.CharField(max_length=255, verbose_name="外网IP地址", null=True, blank=True) 
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品", null=True, blank=True)
    labels = models.ManyToManyField(to=Label, related_name="ins_labels", verbose_name="标签", blank=True)
    instance_type = models.ForeignKey(to=InstanceType, on_delete=models.PROTECT, verbose_name="实例类型", null=True, blank=True)
    use_public_ip = models.IntegerField(default=0, verbose_name="是否通过外网IP监控")  # 0: 内网监控 1: 外网监控
    enable = models.IntegerField(default=1, verbose_name="是否禁止")  # 1: 启用 0: 禁止
    server_group = models.ForeignKey(to=ServerGroup, on_delete=models.PROTECT, verbose_name="关联监控采集组", null=True, blank=True)

    def __str__(self):
        return self.name


class InstanceSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True, read_only=True)
    instance_type__name = serializers.CharField(source="instance_type.name", read_only=True)
    product__name = serializers.CharField(source="product.name", read_only=True)
    server_group__name = serializers.CharField(source="server_group.name", read_only=True)

    class Meta:
        model = Instance
        fields = "__all__"


class InstanceFilter(FilterSet):
    class Meta:
        model = Instance
        fields = {
            "id": ["exact", "in"],
            "enable": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "endpoint": ["exact", "in", "contains"],
            "instance_type__name": ["exact", "in", "contains"],
            "private_ip": ["exact", "in", "contains"],
            "public_ip": ["exact", "in", "contains"],
            "product__id": ["exact", "in"],
            "product__name": ["exact", "in", "contains"],
            "server_group__id": ["exact", "in"],
            "server_group__name": ["exact", "in", "contains"],
        }


class InstanceViewSet(viewsets.ModelViewSet):
    queryset = Instance.objects.all().order_by("id")
    filter_class = InstanceFilter
    serializer_class = InstanceSerializer
