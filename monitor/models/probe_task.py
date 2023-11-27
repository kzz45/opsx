import json
from django.db import models
from django.db.models import Q
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers
from public.models.product import Product
from monitor.models.probe import Probe


class ProbeTask(BaseModel):
    class Meta:
        verbose_name_plural = "探测任务"

    name = models.CharField(max_length=255, verbose_name="名称")
    mode = models.CharField(max_length=36, verbose_name="探测类型", default="http")  # http,tcp,ping
    interval = models.IntegerField(default=60, verbose_name="间隔时间")
    timeout = models.IntegerField(default=30, verbose_name="超时时间")
    target = models.CharField(max_length=255, verbose_name="目标", default="")
    labels = models.TextField(default=json.dumps([]), verbose_name="标签", blank=True)
    probe = models.ManyToManyField(to=Probe, verbose_name="探测节点")
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品", null=True)

    def __str__(self):
        return self.name


class ProbeTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProbeTask
        fields = "__all__"


class ProbeTaskFilter(FilterSet):
    class Meta:
        model = ProbeTask
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class ProbeTaskViewSet(viewsets.ModelViewSet):
    queryset = ProbeTask.objects.all().order_by("id")
    filter_class = ProbeTaskFilter
    serializer_class = ProbeTaskSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(product__user_group__users__id=self.request.user.id)).filter(Q(product__name="公共"))
