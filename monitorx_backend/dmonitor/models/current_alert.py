from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from dmonitor.models.silence import Silence
from dmonitor.models.ticket import Ticket
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class CurrentAlert(BaseModel):
    name = models.CharField(max_length=255, verbose_name="当前告警名称")
    fingerprint = models.CharField(max_length=255, verbose_name="指纹", null=True, default=None)
    job = models.CharField(max_length=255, verbose_name="Job", null=True, default=None)
    instance_type = models.CharField(max_length=255, verbose_name="实例类型", null=True, default=None)
    instance_name = models.CharField(max_length=255, verbose_name="实例名称", null=True, default=None)
    ipaddr = models.CharField(max_length=255, verbose_name="IP地址", null=True, default=None)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品")
    endpoint = models.CharField(max_length=255, verbose_name="端点")
    level = models.CharField(max_length=36, verbose_name="级别")
    state = models.CharField(max_length=36, verbose_name="状态")
    silence = models.ForeignKey(to=Silence, on_delete=models.PROTECT, verbose_name="静默维护", null=True, default=None)
    receivers = models.CharField(max_length=255, verbose_name="接收人", null=True, default=None)
    labels = models.TextField(verbose_name="标签", null=True, default=None)
    graph = models.TextField(verbose_name="图", null=True, default=None)
    summary = models.TextField(verbose_name="概括")
    description = models.TextField(verbose_name="描述", null=True, default=None)
    start = models.IntegerField(verbose_name="开始时间")
    update = models.IntegerField(verbose_name="更新时间")
    value = models.FloatField(verbose_name="值")
    ticket = models.ForeignKey(to=Ticket, on_delete=models.PROTECT, verbose_name="故障记录", null=True, default=None)
    checked = models.IntegerField(default=0, verbose_name="")
    deleted = models.IntegerField(default=0, verbose_name="是否删除")  # 1: 删除
    deleted_ts = models.IntegerField(default=0, verbose_name="删除时间")

    def __str__(self):
        return self.name


class CurrentAlertSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="product.id", read_only=True)

    class Meta:
        model = CurrentAlert
        fields = "__all__"


class CurrentAlertFilter(FilterSet):
    class Meta:
        model = CurrentAlert
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            'silence': ['exact', 'in', 'isnull'],
            "fingerprint": ["exact", "in", "contains"],
            "product__id": ["exact", "in", "contains"],
            "product__name": ["exact", "in", "contains"],
        }


class CurrentAlertViewSet(viewsets.ModelViewSet):
    queryset = CurrentAlert.objects.all().order_by("id")
    filter_class = CurrentAlertFilter
    serializer_class = CurrentAlertSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset.filter(deleted=0)
