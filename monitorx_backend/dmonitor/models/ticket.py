from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Ticket(BaseModel):
    name = models.CharField(max_length=255, verbose_name="故障记录名称")
    classification = models.CharField(max_length=255, verbose_name="")
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品")
    level = models.CharField(max_length=255, verbose_name="级别")
    state = models.IntegerField(default=0, verbose_name="状态")  # 0: 待解决 1: 处理中 2: 已解决
    start = models.IntegerField(verbose_name="开始时间")
    end = models.IntegerField(default=None, null=True, verbose_name="结束时间")
    duration = models.IntegerField(default=None, null=True, verbose_name="耗时")
    reason = models.TextField(default=None, null=True, verbose_name="原因")
    result = models.TextField(default=None, null=True, verbose_name="处理结果")
    users = models.TextField(default='', blank=True, verbose_name="用户")

    def __str__(self):
        return self.name


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class TicketFilter(FilterSet):
    class Meta:
        model = Ticket
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().order_by("id")
    filter_class = TicketFilter
    serializer_class = TicketSerializer
