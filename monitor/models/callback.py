from django.db import models
from django.db.models import Q
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers
from public.models.product import Product
from public.models.factory import Factory


class Callback(BaseModel):
    class Meta:
        verbose_name_plural = "告警回调"

    name = models.CharField(max_length=255, verbose_name="名称")
    types = models.IntegerField(default=1, verbose_name="回调类型")  # 1: cms 2：event
    robot = models.CharField(max_length=255, verbose_name="机器人")
    check_duration = models.IntegerField(verbose_name="检查周期", default=60)
    silence_duration = models.IntegerField(verbose_name="静默周期", default=600)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="关联产品")
    factory = models.ForeignKey(to=Factory, on_delete=models.CASCADE, verbose_name="关联云厂商")

    def __str__(self):
        return self.name


class CallbackSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)
    factory__name = serializers.CharField(source="factory.name", read_only=True)

    class Meta:
        model = Callback
        fields = "__all__"


class CallbackFilter(FilterSet):
    class Meta:
        model = Callback
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "robot": ["exact", "in", "contains"],
            "product__name": ["exact", "in", "contains"],
            "factory__name": ["exact", "in", "contains"],
        }


class CallbackViewSet(viewsets.ModelViewSet):
    queryset = Callback.objects.all().order_by("id")
    filter_class = CallbackFilter
    serializer_class = CallbackSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(product__user_group__users__id=self.request.user.id))
