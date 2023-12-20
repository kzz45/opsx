from django.db import models
from dmonitor.models.base import BaseModel
from dmonitor.models.label import Label
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class ServerGroup(BaseModel):
    name = models.CharField(max_length=255, verbose_name="名称")
    mode = models.IntegerField(default=0, verbose_name="分组模式")  # 0: 自定义分组 1: API分组
    policy = models.TextField(default=None, verbose_name="分组策略", null=True)
    labels = models.ManyToManyField(to=Label, related_name="sg_lables", verbose_name="分组上的标签", blank=True)

    def __str__(self):
        return self.name


class ServerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerGroup
        fields = "__all__"


class ServerGroupFilter(FilterSet):
    class Meta:
        model = ServerGroup
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class ServerGroupViewSet(viewsets.ModelViewSet):
    queryset = ServerGroup.objects.all().order_by("id")
    filter_class = ServerGroupFilter
    serializer_class = ServerGroupSerializer
