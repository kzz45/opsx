from django.db import models
from dops.models import BaseModel
from dcmdb.models.zone import Zone
from dcmdb.models.vpc import VPC
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Subnet(BaseModel):
    class Meta:
        verbose_name_plural = "子网"

    subnet_id = models.CharField(
        max_length=255, verbose_name="子网名称", default="")
    name = models.CharField(max_length=255, verbose_name="子网名称")
    alias_name = models.CharField(
        max_length=255, verbose_name="子网名称描述", default="", null=True, blank=True)
    desc = models.CharField(
        max_length=255, verbose_name="子网描述", null=True, blank=True)
    cidr_block = models.CharField(
        max_length=255, verbose_name="CIDR", null=True, blank=True)
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    available_ip_count = models.IntegerField(default=0, verbose_name="可用IP数量")
    vpc = models.ForeignKey(to=VPC, on_delete=models.PROTECT,
                            verbose_name="关联的VPC", null=True, blank=True)
    zone = models.ForeignKey(
        to=Zone, on_delete=models.CASCADE, verbose_name="关联可用区", null=True, blank=True)
    resource_auto_sync = models.IntegerField(
        default=0, verbose_name='自动同步资源标记')

    def __str__(self):
        return self.name


class SubnetSerializer(serializers.ModelSerializer):
    vpc__vpc_name = serializers.CharField(source="vpc.name", read_only=True)
    vpc__vpc_id = serializers.CharField(source="vpc.vpc_id", read_only=True)
    zone__name = serializers.CharField(source="zone.name", read_only=True)
    zone__zone_id = serializers.CharField(
        source="zone.zone_id", read_only=True)
    factory__name = serializers.CharField(
        source="vpc.factory.name", read_only=True)

    class Meta:
        model = Subnet
        fields = "__all__"


class SubnetFilter(FilterSet):
    class Meta:
        model = Subnet
        fields = {
            "id": ["exact", "in"],
            "is_default": ["exact", "in"],
            "subnet_id": ["exact", "in", "contains"],
            "name": ["exact", "in", "contains"],
            "vpc": ["exact", "in"],
            "vpc__vpc_id": ["exact", "in"],
            "vpc__id": ["exact", "in"],
            "vpc__name": ["exact", "in", "contains"],
            "vpc__factory": ["exact", "in"],
            "zone__zone_id": ["exact", "in"],
            "cidr_block": ["exact", "in", "contains"]
        }


class SubnetViewSet(viewsets.ModelViewSet):
    queryset = Subnet.objects.all().order_by("-id")
    filter_class = SubnetFilter
    serializer_class = SubnetSerializer
