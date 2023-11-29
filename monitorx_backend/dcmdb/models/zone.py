from django.db import models
from dops.models import BaseModel
from dcmdb.models.region import Region
from dcmdb.models.factory import Factory
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Zone(BaseModel):
    class Meta:
        verbose_name_plural = "可用区"

    zone_type_choices = (("machine", "machine"), ("redis", "redis"), ("mysql", "mysql"))
    zone_id = models.CharField(max_length=255, verbose_name="可用区ID", default="")
    name = models.CharField(max_length=255, verbose_name="可用区名称", blank=True)
    desc = models.CharField(max_length=255, verbose_name="可用区描述", null=True, blank=True)
    zone_type = models.CharField(max_length=255, verbose_name="可用区类型", choices=zone_type_choices, null=True, blank=True)
    region = models.ForeignKey(to=Region, on_delete=models.PROTECT, verbose_name="关联的地域", null=True, blank=True)
    factory = models.ForeignKey(to=Factory, on_delete=models.CASCADE, verbose_name="厂商", null=True, blank=True)

    def __str__(self):
        return self.zone_id


class ZoneSerializer(serializers.ModelSerializer):
    region__name = serializers.CharField(source="region.name", read_only=True)
    factory__name = serializers.CharField(source="region.factory.name", read_only=True)

    class Meta:
        model = Zone
        fields = "__all__"


class ZoneFilter(FilterSet):
    class Meta:
        model = Zone
        fields = {
            "id": ["exact", "in"],
            "zone_id": ["exact", "in", "contains"],
            "name": ["exact", "in", "contains"],
            "region": ["exact", "in"],
            "region__region_id": ["exact", "in", 'isnull'],
            "factory__id": ["exact", "in"],
            "region__name": ["exact", "in", "contains"],
            "factory__name": ["exact", "in", "contains"],
        }


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all().order_by("-id")
    filter_class = ZoneFilter
    serializer_class = ZoneSerializer
