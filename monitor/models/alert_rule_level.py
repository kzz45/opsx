from django.db import models
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers


class AlertRuleLevel(BaseModel):
    class Meta:
        verbose_name_plural = "规则等级"

    name = models.CharField(max_length=255, verbose_name="名称")
    desc = models.CharField(max_length=255, verbose_name="别名", null=True)

    def __str__(self):
        return self.name


class AlertRuleLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlertRuleLevel
        fields = "__all__"


class AlertRuleLevelFilter(FilterSet):
    class Meta:
        model = AlertRuleLevel
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class AlertRuleLevelViewSet(viewsets.ModelViewSet):
    queryset = AlertRuleLevel.objects.all().order_by("name")
    filter_class = AlertRuleLevelFilter
    serializer_class = AlertRuleLevelSerializer
