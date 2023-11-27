from django.db import models
from django.db.models import Q
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from monitor.models.labels import Labels
from public.models.product import Product
from monitor.models.alert_rule import AlertRule
from django.contrib.auth.models import User


class AlertRuleChild(BaseModel):
    class Meta:
        verbose_name_plural = "告警子规则"

    name = models.CharField(max_length=255, verbose_name="子规则名称")
    interval = models.IntegerField(verbose_name="持续时间", default=180)
    expression = models.TextField(verbose_name="promql 表达式", default="")
    record = models.TextField(verbose_name="记录规则", default="", blank=True)
    op = models.CharField(max_length=255, verbose_name="操作符", default="")
    value = models.IntegerField(verbose_name="阈值", default=0)
    enable = models.BooleanField(verbose_name="是否启用", default=True)
    is_cover = models.BooleanField(verbose_name="是否覆盖父规则", default=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="添加者", null=True)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品", null=True)
    labels = models.ManyToManyField(to=Labels, related_name="child_rule_labels", verbose_name="额外标签", blank=True)
    alert_rule = models.ForeignKey(to=AlertRule, on_delete=models.CASCADE, verbose_name="父规则")

    def __str__(self):
        return self.name


class AlertRuleChildSerializer(serializers.ModelSerializer):
    user__first_name = serializers.CharField(source="user.first_name", read_only=True)
    product__name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = AlertRuleChild
        fields = "__all__"


class AlertRuleChildFilter(FilterSet):
    class Meta:
        model = AlertRuleChild
        fields = {
            "id": ["exact", "in"],
            "alert_rule": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class AlertRuleChildViewSet(viewsets.ModelViewSet):
    queryset = AlertRuleChild.objects.all().order_by("id")
    filter_class = AlertRuleChildFilter
    serializer_class = AlertRuleChildSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(product__user_group__users__id=self.request.user.id)).filter(Q(product__name="公共"))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        child_rule_obj = serializer.save()
        child_rule_obj.user = self.request.user
        child_rule_obj.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
