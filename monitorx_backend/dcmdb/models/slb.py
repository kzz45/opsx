from django.db import models
from dops.models import BaseModel
from dcmdb.models.vpc import VPC
from dcmdb.models.region import Region
from dcmdb.models.factory import Factory
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet
from dcmdb.models.project import Project
from dcmdb.models.product import Product
from rest_framework.decorators import action
from django.http import JsonResponse


class SLB(BaseModel):
    class Meta:
        verbose_name_plural = "负载均衡"

    slb_id = models.CharField(max_length=512, verbose_name="负载均衡ID")
    address = models.CharField(max_length=255, verbose_name="地址")
    name = models.CharField(max_length=255, verbose_name="名称")
    status = models.CharField(
        max_length=255, verbose_name="状态", default="Active", null=True, blank=True)
    network_type = models.CharField(max_length=255, verbose_name="网络类型")
    vpc = models.ForeignKey(to=VPC, on_delete=models.CASCADE,
                            verbose_name="关联的VPC", null=True, blank=True)
    region = models.ForeignKey(
        to=Region, on_delete=models.CASCADE, verbose_name="地域", null=True, blank=True)
    factory = models.ForeignKey(
        to=Factory, on_delete=models.CASCADE, verbose_name="厂商", null=True, blank=True)
    product = models.ForeignKey(
        to=Product, on_delete=models.PROTECT, verbose_name="管理产品", null=True, blank=True)
    project = models.ForeignKey(to=Project, related_name="slb_list",
                                on_delete=models.PROTECT, verbose_name="项目", null=True, blank=True)
    gcp_project_id = models.CharField(
        max_length=255, verbose_name="gcp_project_id", null=True, blank=True)

    def __str__(self):
        return self.address


class SLBSerializer(serializers.ModelSerializer):
    vpc__vpc_id = serializers.CharField(source="vpc.vpc_id", read_only=True)
    vpc__name = serializers.CharField(source="vpc.name", read_only=True)
    region__name = serializers.CharField(source="region.name", read_only=True)
    region__region_id = serializers.CharField(
        source="region.region_id", read_only=True)
    factory__name = serializers.CharField(
        source="factory.name", read_only=True)
    product__name = serializers.CharField(
        source="product.name", read_only=True)
    project__name = serializers.CharField(
        source="project.name", read_only=True)
    factory__kms_account = serializers.CharField(
        source="factory.kms_account", read_only=True)

    class Meta:
        model = SLB
        fields = "__all__"


class SLBFilter(FilterSet):
    class Meta:
        model = SLB
        fields = {
            "id": ["exact", "in"],
            "slb_id": ["exact", "in", "contains"],
            "address": ["exact", "in", "contains"],
            "name": ["exact", "in", "contains"],
            "factory__name": ["exact", "in", "contains", "startswith"],
            "project__id": ["isnull", "exact", "in", "contains"],
            "product__id": ["exact", "in", "contains"],
        }


class SLBViewSet(viewsets.ModelViewSet):
    queryset = SLB.objects.all().order_by("id")
    filter_class = SLBFilter
    serializer_class = SLBSerializer

    @action(detail=False, methods=['POST'], name='update_loadbalancer_status')
    def update_loadbalancer_status(self, request):
        status_map = request.data.get("status_map", {})
        lbs_id = status_map.keys()
        lbs = SLB.objects.filter(slb_id__in=list(lbs_id))
        for lb in lbs:
            lb.status = status_map[lb.slb_id]
            lb.save()
        return JsonResponse({"success": 0}, safe=False)
