from django.db import models
from dcmdb.models.user_group import UserGroup
from dops.models import BaseModel
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Product(BaseModel):
    class Meta:
        verbose_name_plural = "产品"

    name = models.CharField(max_length=255, verbose_name="产品名称", unique=True)
    desc = models.CharField(max_length=255, verbose_name="产品描述", null=True)
    external_id = models.CharField(max_length=255, verbose_name="产品id", null=True)
    user_group = models.ForeignKey(to=UserGroup, on_delete=models.CASCADE, verbose_name="用户组", null=True)

    def __str__(self):
        return self.name


class ProductSerializer(serializers.ModelSerializer):
    user_group__name = serializers.CharField(source="user_group.name", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "external_id": ["exact", "in", "contains"],
        }


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    filter_class = ProductFilter
    serializer_class = ProductSerializer
