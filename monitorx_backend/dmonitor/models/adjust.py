# 告警规则微调

import json
from django.db import models
from dmonitor.models.base import BaseModel
from dmonitor.models.alert_rule import AlertRule
from dcmdb.models.product import Product
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet
from django.contrib.auth import get_user_model
User = get_user_model()


class AdJust(BaseModel):
    alert_rule = models.ForeignKey(to=AlertRule, related_name="ar_children", on_delete=models.PROTECT, verbose_name="告警规则")
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品", blank=True)
    match = models.TextField(default=json.dumps([]), verbose_name="匹配规则")
    op = models.CharField(max_length=255, default="", verbose_name="表达式")
    value = models.IntegerField(default=0, verbose_name="值")
    is_cover = models.IntegerField(default=1, verbose_name="是否覆盖")  # 1 为覆盖父规则
    level = models.CharField(max_length=255, verbose_name="级别")
    parent = models.IntegerField(default=1, verbose_name="父子规则")
    create_user = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name="创建者", null=True, blank=True)


class AdJustSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)
    create_user__username = serializers.CharField(source="create_user.username", read_only=True)
    create_user__first_name = serializers.CharField(source="create_user.first_name", read_only=True)

    class Meta:
        model = AdJust
        fields = "__all__"


class AdJustFilter(FilterSet):
    class Meta:
        model = AdJust
        fields = {
            "id": ["exact", "in"],
            "alert_rule__id": ["exact", "in"],
            "product__id": ["exact", "in"],
            "create_user__id": ["exact", "in"],
        }


class AdJustViewSet(viewsets.ModelViewSet):
    queryset = AdJust.objects.all().order_by("id")
    filter_class = AdJustFilter
    serializer_class = AdJustSerializer
