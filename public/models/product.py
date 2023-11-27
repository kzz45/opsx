from django.db import models
from django.db.models import Q
from public.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from public.models.user_group import UserGroup


class Product(BaseModel):
    class Meta:
        verbose_name_plural = "产品"

    name = models.CharField(max_length=255, verbose_name="产品名称", default="")
    desc = models.CharField(max_length=255, verbose_name="产品描述", default="")
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
        }


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    filter_class = ProductFilter
    serializer_class = ProductSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(user_group__users__id=self.request.user.id))

    def create(self, request, *args, **kwargs):
        # 只有超管可以新增一个产品
        if not self.request.user.is_superuser:
            msg = {"status": False, "msg": "you don't have permission"}
            return Response(data=msg, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
