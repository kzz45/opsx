from django.db import models
from django.db.models import Q
from monitor.models.base import BaseModel
from rest_framework.decorators import action
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from monitor.models.alert_rule_type import AlertRuleType
from monitor.models.alert_rule_level import AlertRuleLevel
from monitor.models.labels import Labels
from public.models.product import Product
from django.contrib.auth.models import User


class AlertRule(BaseModel):
    class Meta:
        verbose_name_plural = "告警规则"

    name = models.CharField(max_length=255, verbose_name="告警规则名称")
    interval = models.IntegerField(verbose_name="持续时间", default=180)
    expression = models.TextField(verbose_name="promql 表达式", default="")
    record = models.TextField(verbose_name="记录规则", default="", blank=True)
    op = models.CharField(max_length=255, verbose_name="操作符", default="")
    value = models.IntegerField(verbose_name="阈值", default=0)
    mode = models.IntegerField(verbose_name="模式", default=0)
    summary = models.TextField(verbose_name="告警消息", default="", blank=True)
    description = models.TextField(verbose_name="告警描述", default="", blank=True)
    enable = models.BooleanField(verbose_name="是否启用", default=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="添加者", null=True)
    labels = models.ManyToManyField(to=Labels, related_name="alert_rule_labels", verbose_name="额外标签", blank=True)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品", null=True)
    alert_rule_type = models.ForeignKey(to=AlertRuleType, on_delete=models.PROTECT, verbose_name="规则类型", null=True)
    alert_rule_level = models.ForeignKey(to=AlertRuleLevel, on_delete=models.CASCADE, verbose_name="规则等级", null=True)

    def __str__(self):
        return self.name


class AlertRuleSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)
    alert_rule_type__name = serializers.CharField(source="alert_rule_type.name", read_only=True)
    alert_rule_level__name = serializers.CharField(source="alert_rule_level.name", read_only=True)

    class Meta:
        model = AlertRule
        fields = "__all__"


class AlertRuleFilter(FilterSet):
    class Meta:
        model = AlertRule
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class AlertRuleViewSet(viewsets.ModelViewSet):
    queryset = AlertRule.objects.all().order_by("id")
    filter_class = AlertRuleFilter
    serializer_class = AlertRuleSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(product__user_group__users__id=self.request.user.id)).filter(Q(product__name="公共"))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        alert_rule_obj = serializer.save()
        alert_rule_obj.user = self.request.user
        alert_rule_obj.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=["GET"])
    def get_alert_rules(self, request):
        result = []
        alert_rule_objs = AlertRule.objects.all()
        for alert_rule in alert_rule_objs:
            if alert_rule.enable:
                alert_rule_dict = {
                    "alert": alert_rule.name,
                    "expr": "{} {} {}".format(alert_rule.expression, alert_rule.op, str(alert_rule.value)),
                    "for": str(alert_rule.interval) + "s",
                    "labels": {
                        "level": alert_rule.alert_rule_level.name,
                        "_type": alert_rule.alert_rule_type.name,
                    },
                    "annotations": {
                        "summary": alert_rule.summary,
                        "description": alert_rule.description,
                    }
                }
                result.append(alert_rule_dict)
        from monitor.models.alert_rule_child import AlertRuleChild
        alert_rule_child_objs = AlertRuleChild.objects.all()
        if alert_rule_child_objs:
            for child in alert_rule_child_objs:
                if child.enable:
                    alert_rule_child_dict = {
                        "alert": child.name,
                        "expr": "{} {} {}".format(child.expression, child.op, str(child.value)),
                        "for": str(child.interval) + "s",
                        "labels": {
                            "level": child.alert_rule.alert_rule_level.name,
                            "_type": child.alert_rule.alert_rule_type.name,
                            "_parent_id": child.alert_rule.id,
                            "_parent_name": child.alert_rule.name,
                        },
                        "annotations": {
                            "summary": child.alert_rule.summary,
                            "description": child.alert_rule.description,
                        }
                    }
                    result.append(alert_rule_child_dict)
        return Response(data={"rules": result}, status=status.HTTP_200_OK)
