from django.db import models
from dops.models import BaseModel
from dcmdb.models.factory import Factory
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class RedisFlavor(BaseModel):
    class Meta:
        verbose_name_plural = "Redis机型"

    name = models.CharField(max_length=255, verbose_name="机型名称", unique=True)
    desc = models.CharField(max_length=255, verbose_name="机型描述")
    version = models.CharField(max_length=255, verbose_name="版本")
    framework = models.CharField(max_length=255, verbose_name='架构类型')
    shards = models.IntegerField(default=0, verbose_name="分片数")
    spec = models.IntegerField(default=0, verbose_name="实例规格")
    flavor_id = models.CharField(max_length=255, verbose_name="原始机型")

    def __str__(self):
        return self.name


class RedisFlavorSerializer(serializers.ModelSerializer):

    class Meta:
        model = RedisFlavor
        fields = "__all__"


class RedisFlavorFilter(FilterSet):
    class Meta:
        model = RedisFlavor
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class RedisFlavorViewSet(viewsets.ModelViewSet):
    queryset = RedisFlavor.objects.all().order_by("-id")
    filter_class = RedisFlavorFilter
    serializer_class = RedisFlavorSerializer
