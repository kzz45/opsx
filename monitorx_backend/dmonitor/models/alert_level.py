from django.db import models
from dmonitor.models.base import BaseModel
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class AlertLevel(BaseModel):
    name = models.CharField(max_length=255, verbose_name="名称")
    desc = models.CharField(max_length=255, verbose_name="描述")

    def __str__(self):
        return self.name


class AlertLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlertLevel
        fields = "__all__"


class AlertLevelFilter(FilterSet):
    class Meta:
        model = AlertLevel
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class AlertLevelViewSet(viewsets.ModelViewSet):
    queryset = AlertLevel.objects.all().order_by("id")
    filter_class = AlertLevelFilter
    serializer_class = AlertLevelSerializer
