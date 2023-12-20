from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from dcmdb.models.factory import Factory
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class SLS(BaseModel):
    project_name = models.CharField(max_length=255, verbose_name="SLS名称")
    desc = models.CharField(max_length=255, verbose_name="描述")
    logsearch = models.CharField(max_length=255, verbose_name="日志库名称")
    hide = models.BooleanField(default=False, verbose_name="隐藏侧边栏")
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品", null=True, blank=True)
    factory = models.ForeignKey(to=Factory, on_delete=models.PROTECT, verbose_name="厂商", null=True, blank=True)

    def __str__(self):
        return self.logsearch


class SLSSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)
    factory__name = serializers.CharField(source="factory.name", read_only=True)

    class Meta:
        model = SLS
        fields = "__all__"


class SLSFilter(FilterSet):
    class Meta:
        model = SLS
        fields = {
            "id": ["exact", "in"],
            "project_name": ["exact", "in", "contains"],
            "logsearch": ["exact", "in", "contains"],
            "product__id": ["exact", "in"],
            "product__name": ["exact", "in", "contains"],
            "factory__id": ["exact", "in"],
            "factory__name": ["exact", "in", "contains"],
        }


class SLSViewSet(viewsets.ModelViewSet):
    queryset = SLS.objects.all().order_by("id")
    filter_class = SLSFilter
    serializer_class = SLSSerializer
