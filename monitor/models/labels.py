from django.db import models
from django.db.models import Q
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from public.models.product import Product


class Labels(BaseModel):
    class Meta:
        verbose_name_plural = "对象标签"

    name = models.CharField(max_length=255, verbose_name="名称")
    value = models.CharField(max_length=255, verbose_name="值")
    mode = models.IntegerField(verbose_name="类型", default=0)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="产品")

    def __str__(self):
        return self.name


class LabelsSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Labels
        fields = "__all__"


class LabelsFilter(FilterSet):
    class Meta:
        model = Labels
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class LabelsViewSet(viewsets.ModelViewSet):
    queryset = Labels.objects.all().order_by("name")
    filter_class = LabelsFilter
    serializer_class = LabelsSerializer
