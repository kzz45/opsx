
from django.db import models
from dops.models import BaseModel
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Factory(BaseModel):
    class Meta:
        verbose_name_plural = "厂商"

    name = models.CharField(max_length=255, verbose_name="厂商名称", default="阿里云", unique=True)
    desc = models.CharField(max_length=255, verbose_name="厂商描述", null=True)
    access_id = models.CharField(max_length=255, verbose_name="ACCESS ID", null=True, blank=True)
    access_key = models.CharField(max_length=255, verbose_name="ACCESS KEY", null=True, blank=True)
    rolearn = models.CharField(max_length=255, verbose_name="RoleARN", null=True, blank=True)
    kms_account = models.CharField(max_length=255, verbose_name="kms", null=True, blank=True)

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
