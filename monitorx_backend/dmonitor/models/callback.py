from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from dcmdb.models.factory import Factory
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Callback(BaseModel):
    name = models.CharField(max_length=255, verbose_name="名称")
    types = models.IntegerField(default=1, verbose_name="回调类型")  # 1: cms 2：event
    robot = models.CharField(max_length=255, verbose_name="机器人")
    # check_duration = models.IntegerField(verbose_name="检查周期", default=60)
    # silence_duration = models.IntegerField(verbose_name="静默周期", default=600)
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
