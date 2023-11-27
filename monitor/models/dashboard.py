from django.db import models
from django.db.models import Q
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers
from public.models.product import Product


class Dashboard(BaseModel):
    class Meta:
        verbose_name_plural = "告警大盘"

    name = models.CharField(max_length=255, verbose_name="名称")
    desc = models.CharField(max_length=255, verbose_name="描述", null=True)
    addr = models.CharField(max_length=255, verbose_name="地址")
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="产品")

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
        }


class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all().order_by("id")
    filter_class = DashboardFilter
    serializer_class = DashboardSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(product__user_group__users__id=self.request.user.id))
