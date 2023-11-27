import json
from django.db import models
from django.db.models import Q
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from monitor.models.receiver import Receiver
from monitor.models.alert_route import AlertRoute
from public.models.product import Product
from django.contrib.auth.models import User


class AlertRouteChild(BaseModel):
    class Meta:
        verbose_name_plural = "告警子路由"

    name = models.CharField(max_length=255, verbose_name="子路由名称")
    group_wait = models.IntegerField(default=60, verbose_name="通过...等待")
    group_interval = models.IntegerField(default=60, verbose_name="通过...间隔")
    repeat_interval = models.IntegerField(default=3600, verbose_name="重复...间隔")
    match_re = models.BooleanField(default=False, verbose_name="路由正则")
    match = models.TextField(default=json.dumps([]), verbose_name="精确匹配")
    is_raise = models.IntegerField(default=0, verbose_name="是否继续")
    enable = models.BooleanField(default=True, verbose_name="是否启用")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="添加者", null=True)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品", null=True)
    receiver = models.ManyToManyField(to=Receiver, related_name="child_route_receivers", verbose_name="接收者")
    alert_route = models.ForeignKey(to=AlertRoute, on_delete=models.CASCADE, verbose_name="父路由")

    def __str__(self):
        return self.name


class AlertRouteChildSerializer(serializers.ModelSerializer):
    receiver__list = serializers.SerializerMethodField(read_only=True)
    user__first_name = serializers.CharField(source="user.first_name", read_only=True)
    product__name = serializers.CharField(source="product.name", read_only=True)

    def get_receiver__list(self, obj):
        return [i.name for i in obj.receiver.all()]

    class Meta:
        model = AlertRouteChild
        fields = "__all__"


class AlertRouteChildFilter(FilterSet):
    class Meta:
        model = AlertRouteChild
        fields = {
            "id": ["exact", "in"],
            "alert_route": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class AlertRouteChildViewSet(viewsets.ModelViewSet):
    queryset = AlertRouteChild.objects.all().order_by("id")
    filter_class = AlertRouteChildFilter
    serializer_class = AlertRouteChildSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(product__user_group__users__id=self.request.user.id))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        child_route_obj = serializer.save()
        child_route_obj.user = self.request.user
        child_route_obj.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
