from django.db import models
from dops.models import BaseModel
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet
from dcmdb.models.project import Project
from dcmdb.models.product import Product
from dcmdb.models.factory import Factory
from dcmdb.models.machine_flavor import Flavor
from dcmdb.models.group import Group
from dcmdb.models.zone import Zone
from dcmdb.models.tag import Tag
from rest_framework.decorators import action
from django.http import JsonResponse


class Machine(BaseModel):
    class Meta:
        verbose_name_plural = "机器"
        ordering = ['-update_time']

    machine_status_choices = ((0, "使用中"), (1, "停止"), (2, "已退还"), (3, "升降配完成"))

    external_uuid = models.CharField(max_length=255, verbose_name="外部ID", unique=True)
    external_name = models.CharField(max_length=255, verbose_name="名称", null=True)
    external_hostname = models.CharField(max_length=255, verbose_name="主机名", null=True, blank=True)
    external_status = models.CharField(max_length=255, verbose_name="状态", null=True)
    external_flavor = models.CharField(max_length=255, verbose_name="机型", null=True)
    cpu = models.IntegerField(default=0, verbose_name="CPU")
    mem = models.IntegerField(default=0, verbose_name="内存")
    os_name = models.CharField(max_length=255, verbose_name="系统名称", null=True, blank=True)
    desc = models.CharField(max_length=255, verbose_name="机器描述", null=True, blank=True)
    status = models.IntegerField(verbose_name="机器状态", choices=machine_status_choices, default=0)
    flavor = models.ForeignKey(to=Flavor, on_delete=models.CASCADE, verbose_name="机型", null=True, blank=True)
    public_ip = models.CharField(max_length=255, verbose_name="外网IP", null=True, blank=True)
    private_ip = models.CharField(max_length=255, verbose_name="内网IP", null=True, blank=True)
    subnet = models.CharField(max_length=255, verbose_name="关联子网", null=True, blank=True)
    zone = models.ForeignKey(to=Zone, on_delete=models.PROTECT, verbose_name="可用区", null=True)
    factory = models.ForeignKey(to=Factory, on_delete=models.PROTECT, verbose_name="厂商")
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="管理产品", null=True, blank=True)
    project = models.ForeignKey(to=Project, related_name="machine_list", on_delete=models.PROTECT, verbose_name="项目", null=True, blank=True)
    group = models.ForeignKey(to=Group, related_name="machine_group", on_delete=models.PROTECT, verbose_name="产品分组", null=True, blank=True)
    tags = models.ManyToManyField(to=Tag, related_name="machine_tags", verbose_name="标签", blank=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间", null=True)
    gcp_project_id = models.CharField(max_length=255, verbose_name="gcp_project_id", null=True, blank=True)



    def __str__(self):
        return self.external_uuid



class MachineSerializer(serializers.ModelSerializer):
    zone__name = serializers.CharField(source="zone.name", read_only=True)
    region__name = serializers.CharField(source="zone.region.name", read_only=True)
    region__region_id = serializers.CharField(source="zone.region.region_id", read_only=True)
    project__project_id = serializers.CharField(source="project.project_id", read_only=True)
    factory__name = serializers.CharField(source="factory.name", read_only=True)
    factory__kms_account = serializers.CharField(source="factory.kms_account", read_only=True)
    product__name = serializers.CharField(source="product.name", read_only=True)
    project__name = serializers.CharField(source="project.name", read_only=True)
    group__name = serializers.CharField(source="group.name", read_only=True)

    class Meta:
        model = Machine
        fields = "__all__"


class MachineFilter(FilterSet):
    class Meta:
        model = Machine
        fields = {
            "id": ["exact", "in"],
            "external_uuid": ["exact", "in", "contains", "startswith"],
            "external_name": ["exact", "in", "contains", "startswith"],
            "external_status": ["exact", "in", "icontains"],
            "status": ["exact", "in"],
            "external_hostname": ["exact", "in", "contains", "startswith"],
            "public_ip": ["exact", "in", "contains", "startswith"],
            "private_ip": ["exact", "in", "contains", "startswith"],
            "project": ["exact", "in", "isnull"],
            "group__id": ["exact", "in"],
            "product__id": ["exact", "in", "isnull"],
            "product__name": ["exact", "in", "contains", "startswith"],
            "project__id": ["exact", "in", "isnull"],
            "project__name": ["exact", "in", "contains", "startswith"],
            "project__product__id": ["exact", "in"],
            "project__product__name": ["exact", "in", "contains", "startswith"],
            "zone__region__name": ["exact", "in", "contains", "startswith"],
            "factory": ["exact", "in"],
            "factory__name": ["exact", "in", "contains", "startswith"],
        }


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    filter_class = MachineFilter
    serializer_class = MachineSerializer

    @action(detail=False, methods=['POST'], name='update_instance_status')
    def update_instance_status(self, request):
        status_map = request.data.get("status_map", {})
        instance_type = request.data.get("instance_type", None)
        instances_id = status_map.keys()
        instances = Machine.objects.filter(external_uuid__in=list(instances_id))
        for instance in instances:
            instance.external_status = status_map[instance.external_uuid]
            # instance.status = status_map[instance.external_uuid]
            instance.external_flavor = instance_type if instance_type else instance.external_flavor
            instance.save()
        return JsonResponse({"success": 0}, safe=False)
