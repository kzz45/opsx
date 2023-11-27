from django.db import models
from django.db.models import Q
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers
from monitor.models.server import Server
from public.models.product import Product


class BusinessTask(BaseModel):
    class Meta:
        verbose_name_plural = "业务任务"

    name = models.CharField(max_length=255, verbose_name="任务名称")
    url = models.CharField(max_length=255, verbose_name="URL", default="业务任务URL")
    interval = models.IntegerField(default=60, verbose_name="间隔时间")
    timeout = models.IntegerField(default=50, verbose_name="超时时间")
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="产品", null=True)
    server = models.ForeignKey(to=Server, on_delete=models.CASCADE, verbose_name="采集点", null=True)

    def __str__(self):
        return self.name


class BusinessTaskSerializer(serializers.ModelSerializer):
    server__name = serializers.CharField(source="server.name", read_only=True)
    product__name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = BusinessTask
        fields = "__all__"


class BusinessTaskFilter(FilterSet):
    class Meta:
        model = BusinessTask
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class BusinessTaskViewSet(viewsets.ModelViewSet):
    queryset = BusinessTask.objects.all().order_by("id")
    filter_class = BusinessTaskFilter
    serializer_class = BusinessTaskSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(product__user_group__users__id=self.request.user.id) | Q(product__name="公共"))
