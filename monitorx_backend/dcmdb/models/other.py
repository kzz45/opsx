from django.db import models
from dcmdb.models.region import Region
from dops.models import BaseModel
from dcmdb.models.project import Project
from dcmdb.models.factory import Factory
from dcmdb.models.subnet import Subnet
from dcmdb.models.tag import Tag
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Other(BaseModel):
    class Meta:
        verbose_name_plural = "other"

    other_status_choices = ((0, "空闲中"), (1, "使用中"), (2, "已退还"), (3, "待退还"))

    external_name = models.CharField(max_length=255, verbose_name="名称", null=True, blank=True)
    external_uuid = models.CharField(max_length=255, verbose_name="外部ID", unique=True)
    external_status = models.CharField(max_length=255, verbose_name="状态", null=True, blank=True)
    local_status = models.IntegerField(verbose_name="状态", choices=other_status_choices, default=0)
    instance_type = models.IntegerField(verbose_name="类型", default=0)
    region = models.ForeignKey(to=Region, on_delete=models.CASCADE, verbose_name="", null=True, blank=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, verbose_name="", null=True, blank=True)
    factory = models.ForeignKey(to=Factory, on_delete=models.CASCADE, verbose_name="", null=True, blank=True)

    def __str__(self):
        return self.external_uuid


class OtherSerializer(serializers.ModelSerializer):
    region__name = serializers.CharField(source="region.name", read_only=True)
    factory__name = serializers.CharField(source="factory.name", read_only=True)

    class Meta:
        model = Other
        fields = "__all__"


class OtherFilter(FilterSet):
    class Meta:
        model = Other
        fields = {
            "id": ["exact", "in"],
            "external_name": ["exact", "in", "contains"],
            "external_uuid": ["exact", "in", "contains"],
            "local_status": ["exact", "in"],
            "instance_type": ["exact", "in"],
            "project__id": ["exact", "in", "isnull"],
            "project__name": ["exact", "in", "contains", "startswith"],
            "factory": ["exact", "in"],
            "factory__name": ["exact", "in", "contains", "startswith"],
        }


class OtherViewSet(viewsets.ModelViewSet):
    queryset = Other.objects.all().order_by("-id")
    filter_class = OtherFilter
    serializer_class = OtherSerializer
