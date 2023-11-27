from django.db import models
from django.db.models import Q
from public.models.base import BaseModel
from public.models.product import Product
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers


class Project(BaseModel):
    class Meta:
        verbose_name_plural = "项目"

    name = models.CharField(max_length=255, verbose_name="项目名称")
    desc = models.CharField(max_length=255, verbose_name="项目描述", default="")
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="所属产品", null=True)

    def __str__(self):
        return self.name


class ProjectSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Project
        fields = "__all__"


class ProjectFilter(FilterSet):
    class Meta:
        model = Project
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "product": ["exact", "in"],
            "product__name": ["exact", "in", "contains"],
        }


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("id")
    filter_class = ProjectFilter
    serializer_class = ProjectSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(product__user_group__users__id=self.request.user.id))

    def create(self, request, *args, **kwargs):
        # 只有超管或者项目管理员可以操作这里
        # 检查集群是否有以project为名称的命名空间
        # 如果没有则创建
        # 并且需要在本地的namespace表中写入一条数据
        # 或者在前端操作 这样的话可以指定集群
        return super().create(request, *args, **kwargs)
