from django.db import models
from public.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers


class Factory(BaseModel):
    class Meta:
        verbose_name_plural = "云厂商"

    name = models.CharField(max_length=255, verbose_name="云厂名称")
    desc = models.CharField(max_length=255, verbose_name="云厂描述")
    access_id = models.CharField(max_length=255, verbose_name="AccessID")
    access_key = models.CharField(max_length=255, verbose_name="AccessKey")

    def __str__(self):
        return self.name


class FactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Factory
        fields = "__all__"


class FactoryFilter(FilterSet):
    class Meta:
        model = Factory
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class FactoryViewSet(viewsets.ModelViewSet):
    queryset = Factory.objects.all().order_by("id")
    filter_class = FactoryFilter
    serializer_class = FactorySerializer
