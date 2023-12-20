import json
from django.db import models
from django.core.cache import cache
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from dmonitor.models.instance import Instance
from dmonitor.models.instance_type import InstanceType
from dmonitor.models.server_group import ServerGroup
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Task(BaseModel):
    name = models.CharField(max_length=255, verbose_name="名称")
    instance_type = models.ForeignKey(to=InstanceType, related_name="it_tasks", on_delete=models.PROTECT, verbose_name="实例类型", blank=True)
    match = models.TextField(default=json.dumps({}), verbose_name="匹配规则")
    instances = models.ManyToManyField(to=Instance, verbose_name="实例列表", blank=True)
    interval = models.IntegerField(default=60, verbose_name="间隔时间")
    timeout = models.IntegerField(default=50, verbose_name="超时时间")
    auto = models.IntegerField(default=0, verbose_name="是否自动")
    product = models.ForeignKey(to=Product, related_name="p_tasks", on_delete=models.PROTECT, verbose_name="关联产品", blank=True)
    group = models.CharField(max_length=255, verbose_name="分组", default=None, null=True)
    mode = models.IntegerField(default=0, verbose_name="任务模式")  # 0: 基础任务 1: 业务任务 2：探测任务
    url = models.CharField(max_length=255, verbose_name="URL", default=None, null=True)
    server_group = models.ForeignKey(to=ServerGroup, related_name="sg_tasks", on_delete=models.PROTECT, verbose_name="采集组", default=None, null=True)
    label = models.TextField(default=json.dumps([]), verbose_name="标签")

    def __str__(self):
        return self.name


class TaskSerializer(serializers.ModelSerializer):
    server_group__name = serializers.CharField(source="server_group.name", read_only=True)
    product__name = serializers.CharField(source="product.name", read_only=True)
    instance_type__name = serializers.CharField(source="instance_type.name", read_only=True)
    instances = serializers.SerializerMethodField(read_only=True)
    online_instances = serializers.SerializerMethodField(read_only=True)
    add_ons = serializers.SerializerMethodField(read_only=True)

    def get_instances(self, task):
        return task.instances.count()

    def get_online_instances(self, task):
        if task.instance_type.name == "machine":
            cache_key = 'task_online_instances_{}'.format(task.id)
            if cache.get(cache_key) != None:
                return cache.get(cache_key)
            return 0
        if task.instance_type.name == "kubernetes":
            cache_key = 'task_online_kubernetes_{}'.format(task.id)
            if cache.get(cache_key) != None:
                return cache.get(cache_key)
            return 0

    def get_add_ons(self, task):
        return task.task_addons.count()

    class Meta:
        model = Task
        fields = "__all__"


class TaskFilter(FilterSet):
    class Meta:
        model = Task
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "mode": ["exact", "in"],
        }


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("id")
    filter_class = TaskFilter
    serializer_class = TaskSerializer
    permission_classes = []
