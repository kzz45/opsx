from django.db import models
from rest_framework.response import Response
from dops.models import BaseModel
from dcmdb.models.product import Product
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Group(BaseModel):
    class Meta:
        verbose_name_plural = "分组信息"

    name = models.CharField(max_length=255, verbose_name="分组名称", unique=True)
    desc = models.CharField(max_length=255, verbose_name="分组描述", null=True)
    product = models.ForeignKey(to=Product, related_name="group_list", on_delete=models.PROTECT, verbose_name="所属产品", null=True)

    def __str__(self):
        return self.name


class GroupSerializer(serializers.ModelSerializer):
    product__id = serializers.IntegerField(source="product.id", read_only=True)
    product__name = serializers.CharField(source="product.name", read_only=True)

    # machine_list = serializers.SerializerMethodField('get_machine_list', read_only=True)
    # machine_group = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # def get_machine_list(self, obj):
    #     from dcmdb.models.machine import Machine, MachineSerializer
    #     machine_querysets = Machine.objects.filter(group__id=obj.id)
    #     machine_serializer = MachineSerializer(instance=machine_querysets, many=True)
    #     return machine_serializer.data

    class Meta:
        model = Group
        fields = "__all__"


class GroupFilter(FilterSet):
    class Meta:
        model = Group
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "product__id": ["exact", "in"],
            "product__name": ["exact", "in", "contains"],
        }


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("id")
    filter_class = GroupFilter
    serializer_class = GroupSerializer
