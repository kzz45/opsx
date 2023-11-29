from dcmdb.models.factory import Factory
from django.db import models
from dops.models import BaseModel
from dcmdb.models.region import Region
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class VPC(BaseModel):
    class Meta:
        verbose_name_plural = "网络"

    vpc_id = models.CharField(max_length=255, verbose_name="VPC ID", default="")
    name = models.CharField(max_length=255, verbose_name="VPC名称", blank=True)
    desc = models.CharField(max_length=255, verbose_name="VPC描述", null=True, blank=True)
    cidr_block = models.CharField(max_length=255, verbose_name="网段", null=True, blank=True)
    region = models.ForeignKey(to=Region, on_delete=models.PROTECT, verbose_name="关联的地域", null=True, blank=True)
    factory = models.ForeignKey(to=Factory, on_delete=models.CASCADE, verbose_name="厂商", null=True, blank=True)

    def __str__(self):
        return self.name


class VPCSerializer(serializers.ModelSerializer):
    region__name = serializers.CharField(source="region.name", read_only=True)
    region__region_id = serializers.CharField(source="region.region_id", read_only=True)
    factory__name = serializers.CharField(source="factory.name", read_only=True)

    class Meta:
        model = VPC
        fields = "__all__"


class VPCFilter(FilterSet):
    class Meta:
        model = VPC
        fields = {
            "id": ["exact", "in"],
            "vpc_id": ["exact", "in", "contains"],
            "name": ["exact", "in", "contains"],
            "region__id": ["exact", "in", 'isnull'],
            "region__name": ["exact", "in", "contains"],
            "factory__name": ["exact", "in", "contains", "startswith"],
            "region__region_id": ["exact", "in"],
            "factory": ["exact", "in"],
            "factory__id": ["exact", "in"],
        }


class VPCViewSet(viewsets.ModelViewSet):
    queryset = VPC.objects.all().order_by("-id")
    filter_class = VPCFilter
    serializer_class = VPCSerializer
