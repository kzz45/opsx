from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Dashboard(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Dashboard名称")
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品")
    url = models.TextField(verbose_name="URL地址")
    describe = models.TextField(default=None, null=True, verbose_name="描述")

    def __str__(self):
        return self.name


class DashboardSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Dashboard
        fields = "__all__"


class DashboardFilter(FilterSet):
    class Meta:
        model = Dashboard
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "product__id": ["exact", "in"],
            "product__name": ["exact", "in", "contains"],
        }


class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all().order_by("id")
    filter_class = DashboardFilter
    serializer_class = DashboardSerializer
