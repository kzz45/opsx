from django.db import models
from dops.models import BaseModel
from dcmdb.models.product import Product
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Tag(BaseModel):
    class Meta:
        verbose_name_plural = "标签"
    name = models.CharField(max_length=255, verbose_name="标签名称", unique=True)
    desc = models.CharField(max_length=255, verbose_name="标签描述", null=True)
    product = models.ForeignKey(to=Product, related_name="cmdb_tags",
                                on_delete=models.CASCADE, verbose_name="关联产品", null=True, blank=True)

    def __str__(self):
        return self.name


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TagFilter(FilterSet):
    class Meta:
        model = Tag
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "product": ["exact", "in"],
        }


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("-id")
    filter_class = TagFilter
    serializer_class = TagSerializer
