from django.db import models
from dops.models import BaseModel
from dcmdb.models.vpc import VPC
from dcmdb.models.factory import Factory
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet

class Security(BaseModel):
    class Meta:
        verbose_name_plural = "安全组"

    security_id = models.CharField(max_length=255, verbose_name="安全组ID")
    name = models.CharField(max_length=255, verbose_name="安全组名称")
    desc = models.CharField(max_length=255, verbose_name="安全组描述", null=True, blank=True)
    vpc = models.ForeignKey(to=VPC, on_delete=models.CASCADE, verbose_name="关联的VPC")
    factory = models.ForeignKey(to=Factory, on_delete=models.PROTECT, verbose_name="厂商", null=True)

    def __str__(self):
        return self.security_id


class SecuritySerializer(serializers.ModelSerializer):
    vpc__vpc_id = serializers.CharField(source="vpc.vpc_id", read_only=True)
    vpc__name = serializers.CharField(source="vpc.name", read_only=True)

    class Meta:
        model = Security
        fields = "__all__"


class SecurityFilter(FilterSet):
    class Meta:
        model = Security
        fields = {
            "id": ["exact", "in"],
            "vpc": ["exact", "in"],
            "security_id": ["exact", "in", "contains"],
            "name": ["exact", "in", "contains"],
            "factory__id": ["exact", "in"],
            "vpc__vpc_id": ["exact", "in"]
        }


class SecurityViewSet(viewsets.ModelViewSet):
    queryset = Security.objects.all().order_by("id")
    filter_class = SecurityFilter
    serializer_class = SecuritySerializer
