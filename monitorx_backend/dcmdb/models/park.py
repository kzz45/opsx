from django.db import models
from dops.models import BaseModel
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Park(BaseModel):
    name = models.CharField(max_length=255, verbose_name="园区名称", unique=True)
    building = models.CharField(max_length=255, verbose_name="楼栋", null=True)
    floor = models.CharField(max_length=255, verbose_name="楼层", null=True)

    def __str__(self):
        return self.name


class ParkSerializer(serializers.ModelSerializer):
    park = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Park
        fields = "__all__"


class ParkFilter(FilterSet):
    class Meta:
        model = Park
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class ParkViewSet(viewsets.ModelViewSet):
    queryset = Park.objects.all().order_by("id")
    filter_class = ParkFilter
    serializer_class = ParkSerializer
