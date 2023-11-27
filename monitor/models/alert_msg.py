from django.db import models
from django.db.models import Q
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers
from public.models.product import Product


class AlertMsg(BaseModel):
    class Meta:
        verbose_name_plural = "告警消息"

    name = models.CharField(max_length=255, verbose_name="告警名称")
    instance_type = models.CharField(max_length=255, verbose_name="实例类型")
    instance_name = models.CharField(max_length=255, verbose_name="实例名称")
    ipaddr = models.CharField(max_length=255, verbose_name="IP地址")
    endpoint = models.CharField(max_length=255, verbose_name="endpoint")
    level = models.CharField(max_length=255, verbose_name="级别")
    state = models.CharField(max_length=255, verbose_name="状态")
    graph = models.CharField(max_length=255, verbose_name="图")
    summary = models.CharField(max_length=255, verbose_name="告警消息")
    fingerprint = models.CharField(max_length=255, verbose_name="指纹")
    end_at = models.IntegerField(verbose_name="结束时间", default=0)
    start_at = models.IntegerField(verbose_name="开始时间", default=1)
    receiver = models.CharField(max_length=255, verbose_name="接收人")
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="告警产品")

    def __str__(self):
        return self.name


class AlertMsgSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = AlertMsg
        fields = "__all__"


class AlertMsgFilter(FilterSet):
    class Meta:
        model = AlertMsg
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "endpoint": ["exact", "in", "contains"],
        }


class AlertMsgViewSet(viewsets.ModelViewSet):
    queryset = AlertMsg.objects.all().order_by("-start_at")
    filter_class = AlertMsgFilter
    serializer_class = AlertMsgSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(product__user_group__users__id=self.request.user.id))
