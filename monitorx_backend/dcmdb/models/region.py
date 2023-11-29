from django.db import models
from dops.models import BaseModel
from dcmdb.models.factory import Factory
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Region(BaseModel):
    class Meta:
        verbose_name_plural = "区域"

    region_id = models.CharField(max_length=255, verbose_name="Region ID", default="")
    name = models.CharField(max_length=255, verbose_name="区域名称")
    desc = models.CharField(max_length=255, verbose_name="区域描述", null=True, blank=True)
    factory = models.ForeignKey(to=Factory, on_delete=models.PROTECT, verbose_name="关联厂商", blank=True)

    def __str__(self):
        return self.region_id


class RegionSerializer(serializers.ModelSerializer):
    factory__name = serializers.CharField(source="factory.name", read_only=True)

    class Meta:
        model = Region
        fields = "__all__"


class RegionFilter(FilterSet):
    class Meta:
        model = Region
        fields = {
            "id": ["exact", "in"],
            "region_id": ["exact", "in", "contains"],
            "name": ["exact", "in", "contains"],
            "factory__id": ["exact", "in"],
            "factory__name": ["exact", "in", "contains"],
        }


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all().order_by("id")
    filter_class = RegionFilter
    serializer_class = RegionSerializer
