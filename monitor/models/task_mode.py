from django.db import models
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers


class TaskMode(BaseModel):
    class Meta:
        verbose_name_plural = "任务模式"

    name = models.CharField(max_length=255, verbose_name="名称")
    desc = models.CharField(max_length=255, verbose_name="描述", null=True)
    args = models.CharField(max_length=255, verbose_name="任务默认参数", null=True)

    def __str__(self):
        return self.name


class TaskModeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskMode
        fields = "__all__"


class TaskModeFilter(FilterSet):
    class Meta:
        model = TaskMode
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class TaskModeViewSet(viewsets.ModelViewSet):
    queryset = TaskMode.objects.all().order_by("id")
    filter_class = TaskModeFilter
    serializer_class = TaskModeSerializer
