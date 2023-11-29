from django.db import models
from dops.models import BaseModel
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet
from dcmdb.models.factory import Factory
from dcmdb.models.region import Region


class Image(BaseModel):
    class Meta:
        verbose_name_plural = "机器镜像"

    external_id = models.CharField(max_length=255, verbose_name="镜像ID")
    external_name = models.CharField(max_length=255, verbose_name="镜像名称")
    external_desc = models.CharField(max_length=255, verbose_name="镜像描述", null=True, blank=True)
    external_osname = models.CharField(max_length=255, verbose_name="操作系统", null=True, blank=True)
    image_type = models.CharField(max_length=255, verbose_name="镜像类型", null=True, blank=True)
    local_desc = models.CharField(max_length=255, verbose_name="本地描述", null=True, blank=True)
    region = models.ForeignKey(to=Region, on_delete=models.CASCADE, verbose_name="地区", null=True, blank=True)
    factory = models.ForeignKey(to=Factory, on_delete=models.CASCADE, verbose_name="厂商", null=True, blank=True)
    project_id = models.CharField(max_length=255, verbose_name="GCP project_id", default="", null=True, blank=True)

    def __str__(self):
        return self.external_id


class ImageSerializer(serializers.ModelSerializer):
    region__name = serializers.CharField(source="region.name", read_only=True)
    region__region_id = serializers.CharField(source="region.region_id", read_only=True)
    factory__name = serializers.CharField(source="factory.name", read_only=True)

    class Meta:
        model = Image
        fields = "__all__"


class ImageFilter(FilterSet):
    class Meta:
        model = Image
        fields = {
            "id": ["exact", "in"],
            "external_id": ["exact", "in", "contains"],
            "external_name": ["exact", "in", "contains"],
            "external_desc": ["exact", "in", "contains"],
            "external_osname": ["exact", "in", "contains"],
            "image_type": ["exact", "in", "contains"],
            "region": ["exact", "in"],
            "region__region_id": ["exact", "in"],
            "region__name": ["exact", "in", "contains"],
            "factory": ["exact", "in"],
            "factory__name": ["exact", "in", "contains"],
            "project_id": ["exact", "in", "contains"]
        }


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all().order_by("id")
    filter_class = ImageFilter
    serializer_class = ImageSerializer