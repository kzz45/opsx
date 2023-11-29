from django.db import models
from dmonitor.models.base import BaseModel
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class AlertRuleType(BaseModel):
    name = models.CharField(max_length=255, verbose_name="规则类型")
    desc = models.CharField(max_length=255, verbose_name="规则类型描述", null=True)

    def __str__(self):
        return self.name


class AlertRuleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertRuleType
        fields = "__all__"


class AlertRuleTypeFilter(FilterSet):
    class Meta:
        model = AlertRuleType
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class AlertRuleTypeViewSet(viewsets.ModelViewSet):
    queryset = AlertRuleType.objects.all().order_by("id")
    filter_class = AlertRuleTypeFilter
    serializer_class = AlertRuleTypeSerializer
