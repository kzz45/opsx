from django.db import models
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers


class AlertRuleType(BaseModel):
    class Meta:
        verbose_name_plural = "规则类型"

    name = models.CharField(max_length=255, verbose_name="名称")
    desc = models.CharField(max_length=255, verbose_name="别名", null=True)

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
    queryset = AlertRuleType.objects.all().order_by("name")
    filter_class = AlertRuleTypeFilter
    serializer_class = AlertRuleTypeSerializer
