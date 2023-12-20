from django.db import models
from dops.models import BaseModel
from dcmdb.models.product import Product
from dcmdb.models.subnet import Subnet
from dcmdb.models.tag import Tag
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet
import django_filters

User = get_user_model()


class Project(BaseModel):
    class Meta:
        verbose_name_plural = "项目"

    name = models.CharField(max_length=255, verbose_name="项目名称", unique=True)
    desc = models.CharField(max_length=255, verbose_name="项目描述", null=True)
    admin = models.ForeignKey(to=User, related_name="project_admin_user", on_delete=models.PROTECT, verbose_name="项目负责人", null=True)
    ops_user = models.ForeignKey(to=User, related_name="project_ops_user", on_delete=models.PROTECT, verbose_name="运维负责人", null=True)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="关联产品", null=True)
    project_id = models.CharField(max_length=255, verbose_name="gcp_project_id", null=True, blank=True)
    # tags = models.CharField(max_length=255, verbose_name="标签", null=True, blank=True)
    tags = models.ForeignKey(to=Tag, on_delete=models.CASCADE, verbose_name="标签", null=True, blank=True)
    subnet = models.ForeignKey(to=Subnet, on_delete=models.CASCADE, verbose_name="子网", null=True, blank=True)

    def __str__(self):
        return self.name


class ProjectSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)
    admin__username = serializers.CharField(source="admin.username", read_only=True)
    admin__first_name = serializers.CharField(source="admin.first_name", read_only=True)
    ops_user__username = serializers.CharField(source="ops_user.username", read_only=True)
    ops_user__first_name = serializers.CharField(source="ops_user.first_name", read_only=True)
    subnet__subnet_id = serializers.CharField(source="subnet.subnet_id", read_only=True)

    class Meta:
        model = Project
        fields = "__all__"


class ProjectFilter(FilterSet):

    product = django_filters.CharFilter(method='filter_product')

    def filter_product(self, queryset, name, value):
        if value == '0':
            return queryset
        else:
            return queryset.filter(product=value)

    class Meta:
        model = Project
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "product": ["exact", "in"],
            "product__id": ["exact", "in", "isnull"],
            "product__name": ["exact", "in", "contains"],
            "subnet__subnet_id": ["exact", "in", "contains"],
            "tags": ["exact", "in"],
            "tags__name": ["exact", "in", "contains"],
        }


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("-id")
    filter_class = ProjectFilter
    serializer_class = ProjectSerializer
