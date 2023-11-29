
from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Label(BaseModel):
    name = models.CharField(max_length=255, verbose_name="标签名称")
    value = models.CharField(max_length=255, verbose_name="标签值", null=True)
    mode = models.IntegerField(default=0, verbose_name="标签类型")  # 0: 自定义标签 1: 上报标签 2: 分组标签
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品", null=True)

    def __str__(self):
        return self.name


class LabelSerializer(serializers.ModelSerializer):
    product__name =serializers.CharField(source="product.name", read_only=True)
    class Meta:
        model = Label
        fields = "__all__"


class LabelFilter(FilterSet):
    class Meta:
        model = Label
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all().distinct().order_by("id")
    filter_class = LabelFilter
    serializer_class = LabelSerializer
