from datetime import datetime
from django.db import models
from dops.models import BaseModel
from dcmdb.models.project import Project
from dcmdb.models.factory import Factory
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class DomainCert(BaseModel):
    name = models.CharField(max_length=255, verbose_name="证书名称")
    desc = models.CharField(max_length=255, verbose_name="证书描述", null=True)
    cert_id = models.CharField(max_length=255, verbose_name="证书ID", null=True, blank=True)
    cert_file = models.TextField(verbose_name="证书内容", null=True, blank=True)
    key_file = models.TextField(verbose_name="证书私钥", null=True, blank=True)
    issure_by = models.CharField(max_length=255, verbose_name="提供商")
    valid_to = models.CharField(max_length=255, verbose_name="到期时间")
    factory = models.ForeignKey(to=Factory, on_delete=models.PROTECT, verbose_name="厂商", null=True)


class DomainCertSerializer(serializers.ModelSerializer):
    factory__name = serializers.CharField(source="factory.name", read_only=True)
    valid_days = serializers.SerializerMethodField(read_only=True)

    def get_valid_days(self, obj):
        return (datetime.strptime(obj.valid_to, "%Y-%m-%d") - datetime.now()).days

    class Meta:
        model = DomainCert
        fields = "__all__"


class DomainCertFilter(FilterSet):
    class Meta:
        model = DomainCert
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class DomainCertViewSet(viewsets.ModelViewSet):
    queryset = DomainCert.objects.all().order_by("id")
    filter_class = DomainCertFilter
    serializer_class = DomainCertSerializer
