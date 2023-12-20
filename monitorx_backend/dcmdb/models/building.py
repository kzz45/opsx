from django.db import models
from dcmdb.models.park import Park
from dops.models import BaseModel
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Building(BaseModel):
    name = models.CharField(max_length=255, verbose_name="名称")
    floor = models.CharField(max_length=255, verbose_name="楼层", null=True)
    park = models.ForeignKey(to=Park, related_name="building_park", on_delete=models.CASCADE, verbose_name="园区")

    def __str__(self):
        return self.name


class BuildingSerializer(serializers.ModelSerializer):
    park__name = serializers.CharField(source="park.name", read_only=True)

    class Meta:
        model = Building
        fields = "__all__"


class BuildingFilter(FilterSet):
    class Meta:
        model = Building
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "park": ["exact", "in"],
            "park__name": ["exact", "in", "contains"],
        }


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all().order_by("id")
    filter_class = BuildingFilter
    serializer_class = BuildingSerializer
