
from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class LabelName(BaseModel):
    name = models.CharField(max_length=255, verbose_name="标签名称")
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, default=0)
    mode = models.IntegerField(default=1, verbose_name="标签类型")  # 0：内部标签，1：自定义标签

    def __str__(self):
        return self.name


class LabelNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = LabelName
        fields = "__all__"


class LabelNameFilter(FilterSet):
    class Meta:
        model = LabelName
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class LabelNameViewSet(viewsets.ModelViewSet):
    queryset = LabelName.objects.all().order_by("id")
    filter_class = LabelNameFilter
    serializer_class = LabelNameSerializer
