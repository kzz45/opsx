from django.db import models
from dmonitor.models.base import BaseModel
from dmonitor.models.task import Task
from dmonitor.models.probe import Probe
from dmonitor.models.server_group import ServerGroup
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class AddOn(BaseModel):
    name = models.CharField(max_length=255, verbose_name="名称")
    task = models.ForeignKey(to=Task, related_name="task_addons", on_delete=models.PROTECT, verbose_name="任务")
    scheme = models.CharField(max_length=32, default="http", verbose_name="scheme")  # http or https
    style = models.CharField(max_length=255, default='machine', verbose_name="类型")
    module = models.CharField(max_length=255, default='port', verbose_name="模块")
    port = models.IntegerField(default=None, null=True, verbose_name="端口")
    probe = models.ForeignKey(to=Probe, related_name="probe_addons", on_delete=models.PROTECT, null=True, blank=True, verbose_name="探测")
    probe_args = models.TextField(null=True, blank=True, verbose_name="探测参数")  # 探测类型的话，探测的参数
    args = models.TextField(null=True, blank=True, verbose_name="参数")
    interval = models.IntegerField(default=None, verbose_name="间隔时间")
    timeout = models.IntegerField(default=None, verbose_name="超时时间")
    server_group = models.ForeignKey(to=ServerGroup, related_name="sg_addons", on_delete=models.PROTECT, null=True, blank=True, verbose_name="采集组")
    relabel = models.TextField(default=None, null=True, verbose_name="标签")

    def __str__(self):
        return self.name


class AddOnSerializer(serializers.ModelSerializer):
    task__name = serializers.CharField(source="task.name", read_only=True)
    probe__api = serializers.CharField(source="probe.api", read_only=True)
    server_group__name = serializers.CharField(source="server_group.name", read_only=True)

    class Meta:
        model = AddOn
        fields = "__all__"


class AddOnFilter(FilterSet):
    class Meta:
        model = AddOn
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "task__id": ["exact", "in", "contains"],
            "task__name": ["exact", "in", "contains"],
        }


class AddOnViewSet(viewsets.ModelViewSet):
    queryset = AddOn.objects.all().order_by("id")
    filter_class = AddOnFilter
    serializer_class = AddOnSerializer
