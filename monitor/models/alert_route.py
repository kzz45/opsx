import json
from django.db import models
from django.db.models import Q
from monitor.models.base import BaseModel
from rest_framework.decorators import action
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from monitor.models.receiver import Receiver
from public.models.product import Product
from django.contrib.auth.models import User


class AlertRoute(BaseModel):
    class Meta:
        verbose_name_plural = "告警路由"

    name = models.CharField(max_length=255, verbose_name="路由名称")
    group_by = models.TextField(default=json.dumps(["_product_id", "alertname", "level"]), verbose_name="通过...")
    group_wait = models.IntegerField(default=60, verbose_name="通过...等待")
    group_interval = models.IntegerField(default=60, verbose_name="通过...间隔")
    repeat_interval = models.IntegerField(default=3600, verbose_name="重复...间隔")
    match_re = models.BooleanField(default=False, verbose_name="路由正则")
    match = models.TextField(default=json.dumps([]), verbose_name="精确匹配")
    is_raise = models.IntegerField(default=0, verbose_name="是否继续")
    enable = models.BooleanField(default=True, verbose_name="是否启用")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="添加者", null=True)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品", null=True)
    receiver = models.ManyToManyField(to=Receiver, related_name="alert_route_receivers", verbose_name="接收者")

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
            "name": ["exact", "in", "contains"],
        }


class AlertRouteViewSet(viewsets.ModelViewSet):
    queryset = AlertRoute.objects.all().order_by("id")
    filter_class = AlertRouteFilter
    serializer_class = AlertRouteSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(product__user_group__users__id=self.request.user.id))

    @action(detail=False, methods=["GET"])
    def get_alert_routes(self, request):
        result = {
            "routes": [],
            "receivers": []
        }
        receivers = []
        alert_route_objs = AlertRoute.objects.all()
        for alert_route in alert_route_objs:
            if alert_route.enable:
                match = json.loads(alert_route.match)
                receiver = ",".join([str(i.name) for i in alert_route.receiver.all()])
                receiver_obj = alert_route.receiver.all()
                receivers = [i for i in receiver_obj]
                alert_route_dict = {
                    "name": alert_route.name,
                    "match_re": alert_route.match_re,
                    "match": {i["name"]: i["value"] for i in match["label"]},
                    "receiver": receiver,
                    "group_wait": alert_route.group_wait,
                    "group_interval": alert_route.group_interval,
                    "repeat_interval": alert_route.repeat_interval,
                    "group_by": json.loads(alert_route.group_by),
                    "continue": alert_route.is_raise == 0,
                }
                result["routes"].append(alert_route_dict)
        from monitor.models.alert_route_child import AlertRouteChild
        alert_route_child_objs = AlertRouteChild.objects.all()
        for child in alert_route_child_objs:
            if child.enable:
                parent_match = json.loads(child.alert_route.match)
                parent_match_dict = {i["name"]: i["value"] for i in parent_match["label"]},

                match = json.loads(child.match)
                receiver = ",".join([str(i.name) for i in child.receiver.all()])
                alert_route_child_dict = {
                    "name": child.name,
                    "match_re": child.match_re,
                    "match": {i["name"]: i["value"] for i in match["label"]},
                    "receiver": receiver,
                    "group_wait": child.group_wait,
                    "group_interval": child.group_interval,
                    "repeat_interval": child.repeat_interval,
                    "group_by": json.loads(child.alert_route.group_by),
                    "continue": child.is_raise == 0,
                }
                result["routes"].append(alert_route_child_dict)
        for receiver_obj in set(receivers):
            result["receivers"].append(
                {"name": receiver_obj.name, "webhook": receiver_obj.webhook}
            )
        return Response(data=result, status=status.HTTP_200_OK)
