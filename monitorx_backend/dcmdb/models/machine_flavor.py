from django.db import models
from dops.models import BaseModel
from dcmdb.models.factory import Factory
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Flavor(BaseModel):
    class Meta:
        verbose_name_plural = "机型配置"

    name = models.CharField(max_length=255, verbose_name="机型名称", unique=True)
    desc = models.CharField(
        max_length=255, verbose_name="机型描述", null=True, blank=True)
    flavor_id = models.CharField(
        max_length=255, verbose_name="原始机型", null=True, blank=True)
    cpu = models.IntegerField(default=0, verbose_name="CPU", blank=True)
    mem = models.IntegerField(default=0, verbose_name="内存", blank=True)
    disk = models.IntegerField(default=0, verbose_name="磁盘", blank=True)
    price = models.IntegerField(
        default=0, verbose_name="价格", null=True, blank=True)
    factory = models.ForeignKey(
        to=Factory, on_delete=models.CASCADE, verbose_name="厂商", null=True)

    def __str__(self):
        return self.name


class FlavorSerializer(serializers.ModelSerializer):
    factory__name = serializers.CharField(
        source="factory.name", read_only=True)

    class Meta:
        model = Flavor
        fields = "__all__"


class FlavorFilter(FilterSet):
    class Meta:
        model = Flavor
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "factory": ["exact", "in"],
            "factory__id": ["exact", "in"],

        }


class FlavorViewSet(viewsets.ModelViewSet):
    queryset = Flavor.objects.all().order_by("id")
    filter_class = FlavorFilter
    serializer_class = FlavorSerializer
