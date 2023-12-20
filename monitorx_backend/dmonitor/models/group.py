from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from dmonitor.models.instance import Instance
from dmonitor.models.instance_type import InstanceType
from dmonitor.models.label import Label
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Group(BaseModel):
    name = models.CharField(max_length=255, verbose_name="名称")
    product = models.ForeignKey(to=Product, related_name="p_groups", on_delete=models.PROTECT, verbose_name="产品", null=True)
    mode = models.IntegerField(verbose_name="分组类型", default=1)  # 0: API同步分组 1: 自定义分组 2: 策略分组
    policy = models.TextField(verbose_name="分组策略", null=True, blank=True)
    instances = models.ManyToManyField(to=Instance, related_name="ins_groups", verbose_name="实例", blank=True)
    instance_type = models.ForeignKey(to=InstanceType, related_name="it_groups", on_delete=models.PROTECT, verbose_name="实例类型", null=True)
    labels = models.ManyToManyField(to=Label, verbose_name="标签", blank=True)

    def __str__(self):
        return self.name


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class GroupFilter(FilterSet):
    class Meta:
        model = Group
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("id")
    filter_class = GroupFilter
    serializer_class = GroupSerializer
