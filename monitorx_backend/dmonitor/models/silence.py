# 静默(alert manager)

from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet
from django.contrib.auth import get_user_model
User = get_user_model()


class Silence(BaseModel):
    match = models.TextField(verbose_name="匹配规则", null=True)
    start = models.IntegerField(verbose_name="开始时间", default=0)
    end = models.IntegerField(verbose_name="结束时间", default=0)
    duration = models.IntegerField(verbose_name="耗时", default=0)
    unit = models.CharField(max_length=255, default='s', verbose_name="时间单位")
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品", null=True)
    state = models.IntegerField(default=1, verbose_name="状态")  # 1 生效 0 失效
    describe = models.TextField(verbose_name="描述", null=True)
    source = models.IntegerField(verbose_name="来源", default=0)  # 0 自定义 1 快捷方式
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name="维护人", null=True)


class SilenceSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)
    user__username = serializers.CharField(source="user.username", read_only=True)
    user__first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = Silence
        fields = "__all__"


class SilenceFilter(FilterSet):
    class Meta:
        model = Silence
        fields = {
            "id": ["exact", "in"],
            "state": ["exact", "in"],
            "source": ["exact", "in"],
            "user__id": ["exact", "in"],
            "start": ["exact", "in", "lt", "gt"],
            "end": ["exact", "in", "lt", "gt"],
        }


class SilenceViewSet(viewsets.ModelViewSet):
    queryset = Silence.objects.all().order_by("-id")
    filter_class = SilenceFilter
    serializer_class = SilenceSerializer
