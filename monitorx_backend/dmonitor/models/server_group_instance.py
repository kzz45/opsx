
from django.db import models
from dmonitor.models.base import BaseModel
from dmonitor.models.instance import Instance
from dmonitor.models.server_group import ServerGroup
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class ServerGroupInstance(BaseModel):
    endpoint = models.ForeignKey(to=Instance, on_delete=models.PROTECT, verbose_name="分组下的实例")
    server_group = models.ForeignKey(to=ServerGroup, on_delete=models.PROTECT, verbose_name="服务组", null=True)

    def __str__(self):
        return self.endpoint


class ServerGroupInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerGroupInstance
        fields = "__all__"


class ServerGroupInstanceFilter(FilterSet):
    class Meta:
        model = ServerGroupInstance
        fields = {
            "id": ["exact", "in"],
        }


class ServerGroupInstanceViewSet(viewsets.ModelViewSet):
    queryset = ServerGroupInstance.objects.all().order_by("id")
    filter_class = ServerGroupInstanceFilter
    serializer_class = ServerGroupInstanceSerializer
