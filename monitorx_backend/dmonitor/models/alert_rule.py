from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from dmonitor.models.alert_rule_type import AlertRuleType
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class AlertRule(BaseModel):
    name = models.CharField(max_length=255, verbose_name="告警规则名称")
    level = models.CharField(max_length=255, verbose_name="告警级别")
    interval = models.IntegerField(verbose_name="间隔")
    expression = models.TextField(verbose_name="promql 表达式")
    op = models.CharField(max_length=255, verbose_name="操作符", default="")
    value = models.IntegerField(verbose_name="阈值", default=0)
    summary = models.TextField(verbose_name="告警消息", default='', blank=True)
    mode = models.IntegerField(verbose_name="模式", default=0)  # 0: 基础报警规则 1: 自定义(某个产品下)
    description = models.TextField(default='', blank=True, verbose_name="描述")
    alert_rule_type = models.ForeignKey(to=AlertRuleType, on_delete=models.PROTECT, verbose_name="规则类型", null=True)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品", blank=True)
    # enable = models.BooleanField(default=True, verbose_name="是否启用")

    def __str__(self):
        return self.name


class AlertRuleSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = AlertRule
        fields = "__all__"


class AlertRuleFilter(FilterSet):
    class Meta:
        model = AlertRule
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "alert_rule_type": ["exact", "in"],
        }


class AlertRuleViewSet(viewsets.ModelViewSet):
    queryset = AlertRule.objects.all().order_by("id")
    filter_class = AlertRuleFilter
    serializer_class = AlertRuleSerializer
