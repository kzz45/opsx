import json
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from monitor.models.base import BaseModel
from rest_framework.decorators import action
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from monitor.models.server import Server
from monitor.models.task_mode import TaskMode
from public.models.product import Product
from monitor.models.instance import Instance, InstanceSerializer
from monitor.models.instance_type import InstanceType
from django_redis import get_redis_connection
redis_conn = get_redis_connection("monitor")


class TargetTask(BaseModel):
    class Meta:
        verbose_name_plural = "基础任务"

    name = models.CharField(max_length=255, verbose_name="名称")
    refresh = models.IntegerField(verbose_name="刷新时间", default=300)
    interval = models.IntegerField(verbose_name="间隔时间", default=60)
    timeout = models.IntegerField(verbose_name="超时时间", default=50)
    scheme = models.CharField(max_length=255, default="http", verbose_name="scheme")
    match = models.TextField(default=json.dumps({}), verbose_name="匹配规则")
    labels = models.TextField(default=json.dumps([]), verbose_name="过滤标签")
    port = models.IntegerField(verbose_name="端口", default=2021)
    args = models.TextField(verbose_name="参数", default="")
    relabel = models.TextField(verbose_name="额外标签", default="", blank=True)
    url = models.CharField(max_length=255, verbose_name="URL", default="业务任务URL")
    mode = models.ForeignKey(to=TaskMode, on_delete=models.CASCADE, verbose_name="任务模式", null=True)
    instances = models.ManyToManyField(to=Instance, verbose_name="实例列表", blank=True)
    instance_type = models.ForeignKey(to=InstanceType, on_delete=models.CASCADE, verbose_name="实例类型", null=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="产品", null=True)
    server = models.ForeignKey(to=Server, on_delete=models.CASCADE, verbose_name="采集点", null=True)

    def __str__(self):
        return self.name


class TargetTaskSerializer(serializers.ModelSerializer):
    mode__name = serializers.CharField(source="mode.name", read_only=True)
    product__name = serializers.CharField(source="product.name", read_only=True)
    instance_type__name = serializers.CharField(source="instance_type.name", read_only=True)
    instances_count = serializers.SerializerMethodField(read_only=True)

    def get_instances_count(self, obj):
        return obj.instances.count()

    class Meta:
        model = TargetTask
        fields = "__all__"


class TargetTaskFilter(FilterSet):
    class Meta:
        model = TargetTask
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class TargetTaskViewSet(viewsets.ModelViewSet):
    queryset = TargetTask.objects.all().order_by("id")
    filter_class = TargetTaskFilter
    serializer_class = TargetTaskSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(product__user_group__users__id=self.request.user.id)).filter(Q(product__name="公共"))

    # 获取任务列表
    @action(detail=False, methods=["GET"])
    def get_tasks(self, request):
        server_uuid = request.GET.get("server_uuid", None)
        # print("=" * 20, server_uuid)
        if server_uuid:
            task_info = redis_conn.get('task_{}'.format(server_uuid))
            # print("=" * 20, task_info)
            if task_info:
                return JsonResponse(data=json.loads(task_info), safe=False)
            else:
                return JsonResponse(data=[], safe=False)
        else:
            return JsonResponse(data=[], safe=False)

    # 获取任务下实例列表
    @action(detail=False, methods=["POST"])
    def get_task_instances(self, request):
        task_id = request.data.get("task_id", None)
        if task_id:
            queryset = TargetTask.objects.filter(id=task_id).first().instances.all()
            serializer = InstanceSerializer(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=[], status=status.HTTP_402_PAYMENT_REQUIRED)
