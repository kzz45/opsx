from django.db import models
from dops.models import BaseModel
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Operator(BaseModel):
    name = models.CharField(max_length=255, verbose_name="名称")
    desc = models.CharField(max_length=255, verbose_name="描述", null=True)

    def __str__(self):
        return self.name


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = "__all__"


class OperatorFilter(FilterSet):
    class Meta:
        model = Operator
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class OperatorViewSet(viewsets.ModelViewSet):
    queryset = Operator.objects.all().order_by("id")
    filter_class = OperatorFilter
    serializer_class = OperatorSerializer
