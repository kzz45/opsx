from django.db import models, transaction
from django.db.models import Q
from monitor.models.base import BaseModel
from rest_framework.decorators import action
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from monitor.models.instance_type import InstanceType
from public.models.product import Product
from monitor.models.server import Server
from monitor.models.labels import Labels, LabelsSerializer


class Instance(BaseModel):
    class Meta:
        verbose_name_plural = "监控对象"

    name = models.CharField(max_length=255, verbose_name="名称")
    endpoint = models.CharField(max_length=255, verbose_name="Endpoint", unique=True)
    interval = models.IntegerField(verbose_name="间隔时间", default=60)
    timeout = models.IntegerField(verbose_name="超时时间", default=50)
    monitor_port = models.IntegerField(verbose_name="监控端口", default=2021)
    private_ip = models.CharField(max_length=255, verbose_name="内网IP")
    public_ip = models.CharField(max_length=255, verbose_name="外网IP", null=True)
    use_public_ip = models.BooleanField(default=False, verbose_name="是否使用外网IP")
    enable = models.BooleanField(default=True, verbose_name="是否监控")
    server = models.ForeignKey(to=Server, on_delete=models.CASCADE, verbose_name="采集点", null=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="产品", null=True)
    instance_type = models.ForeignKey(to=InstanceType, on_delete=models.CASCADE, verbose_name="实例类型", null=True)
    labels = models.ManyToManyField(to=Labels, related_name="ins_labels", verbose_name="标签", blank=True)

    def __str__(self):
        return self.endpoint


class InstanceSerializer(serializers.ModelSerializer):
    labels = LabelsSerializer(many=True, read_only=True)
    server__name = serializers.CharField(source="server.name", read_only=True)
    product__name = serializers.CharField(source="product.name", read_only=True)
    instance_type__name = serializers.CharField(source="instance_type.name", read_only=True)

    class Meta:
        model = Instance
        fields = "__all__"


class InstanceFilter(FilterSet):
    class Meta:
        model = Instance
        fields = {
            "id": ["exact", "in"],
            "enable": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "endpoint": ["exact", "in", "contains"],
            "public_ip": ["exact", "in", "contains"],
            "private_ip": ["exact", "in", "contains"],
            "server": ["exact", "in"],
            "server__name": ["exact", "in", "contains"],
            "product": ["exact", "in"],
            "product__name": ["exact", "in", "contains"],
            "instance_type": ["exact", "in"],
            "instance_type__name": ["exact", "in", "contains"],
        }


class InstanceViewSet(viewsets.ModelViewSet):
    queryset = Instance.objects.all().order_by("id")
    filter_class = InstanceFilter
    serializer_class = InstanceSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(product__user_group__users__id=self.request.user.id) | Q(product__name="公共"))

    # 批量录入
    # @action(detail=False, methods=["POST"])
    # def batcj_create(self, request):
    #     instance_type = request.data.get("instance_type", None)
    #     instance_list = request.data.get("instance_list", None)
    #     if instance_type and instance_list:
    #         try:
    #             with transaction.atomic():
    #                 instance_type_obj = InstanceType.objects.filter(id=instance_type).first()
    #                 instance_obj_list = []
    #                 for item in instance_list:
    #                     instance_obj = Instance(
    #                         name=item.name,
    #                         endpoint=item.endpoint,
    #                         private_ip=item.private_ip,
    #                         instance_type=instance_type_obj,
    #                     )
    #                     instance_obj_list.append(instance_obj)
    #                 Instance.objects.bulk_create(instance_obj_list)
    #                 msg = {"status": True, "msg": ""}
    #                 return Response(data=msg, status=status.HTTP_201_CREATED)
    #         except Exception as err:
    #             msg = {"status": False, "msg": repr(err)}
    #             return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         msg = {"status": False, "msg": "missing parameters, need instance_type and instance_list"}
    #         return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
