from django.db import models
from django.db.models import Q
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers
from public.models.product import Product


class Receiver(BaseModel):
    class Meta:
        verbose_name_plural = "告警接收"

    name = models.CharField(max_length=255, verbose_name="名称")
    desc = models.CharField(max_length=255, verbose_name="描述", default="", blank=True)
    channel = models.CharField(max_length=255, verbose_name="通知渠道", default="feishu")
    webhook = models.CharField(max_length=255, verbose_name="webhook地址", default="")
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="产品", null=True)

    def __str__(self):
        return self.name


class ReceiverSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Receiver
        fields = "__all__"


class ReceiverFilter(FilterSet):
    class Meta:
        model = Receiver
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class ReceiverViewSet(viewsets.ModelViewSet):
    queryset = Receiver.objects.all().order_by("id")
    filter_class = ReceiverFilter
    serializer_class = ReceiverSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(product__user_group__users__id=self.request.user.id))
