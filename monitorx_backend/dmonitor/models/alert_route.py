import json
from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from dmonitor.models.user_group import UserGroup, UserGroupSerializer
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class AlertRoute(BaseModel):
    name = models.CharField(max_length=255, verbose_name="路由名称", default="默认路由")
    group_by = models.TextField(default=json.dumps(["_product_id", "alertname", "level"]), verbose_name="通过...")
    group_wait = models.IntegerField(default=60, verbose_name="通过...等待")
    group_interval = models.IntegerField(default=60, verbose_name="通过...间隔")
    repeat_interval = models.IntegerField(default=3600, verbose_name="重复...间隔")
    receiver = models.ManyToManyField(to=UserGroup, related_name="alert_route_receivers", verbose_name="接收者")
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品", default=-1)
    match = models.TextField(default=json.dumps([]), verbose_name="匹配")
    parent = models.IntegerField(default=0, verbose_name="父路由")
    is_raise = models.IntegerField(default=0, verbose_name="是否通知父亲")
    # enable = models.BooleanField(default=True, verbose_name="是否启用")

    def __str__(self):
        return self.name


class AlertRouteSerializer(serializers.ModelSerializer):
    receiver__list = serializers.SerializerMethodField(read_only=True)
    product__name = serializers.CharField(source="product.name", read_only=True)

    def get_receiver__list(self, obj):
        return [i.name for i in obj.receiver.all()]

    class Meta:
        model = AlertRoute
        fields = "__all__"


class AlertRouteFilter(FilterSet):
    class Meta:
        model = AlertRoute
        fields = {
            "id": ["exact", "in"],
            "parent": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "product__id": ["exact", "in"],
            "product__name": ["exact", "in", "contains"],
        }


class AlertRouteViewSet(viewsets.ModelViewSet):
    queryset = AlertRoute.objects.all().order_by("id")
    filter_class = AlertRouteFilter
    serializer_class = AlertRouteSerializer
