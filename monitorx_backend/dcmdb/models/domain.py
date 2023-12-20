from django.db import models
from dops.models import BaseModel
from dcmdb.models.project import Project
from dcmdb.models.factory import Factory
from dcmdb.models.cert import DomainCert
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet

class Domain(BaseModel):
    name = models.CharField(max_length=255, verbose_name="域名名称", unique=True)
    desc = models.CharField(max_length=255, verbose_name="域名描述", null=True)
    dns_server = models.CharField(max_length=255, verbose_name="域名DNS服务器", null=True, blank=True)
    is_ssl = models.BooleanField(default=False, verbose_name="是否加载证书")
    domain_cert = models.ForeignKey(to=DomainCert, on_delete=models.PROTECT, verbose_name="关联的证书", null=True)
    factory = models.ForeignKey(to=Factory, on_delete=models.PROTECT, verbose_name="厂商", null=True)
    project = models.ForeignKey(to=Project, related_name="domain_list", on_delete=models.PROTECT, verbose_name="关联项目", null=True, blank=True)


class DomainSerializer(serializers.ModelSerializer):
    factory__name = serializers.CharField(source="factory.name", read_only=True)

    class Meta:
        model = Domain
        fields = "__all__"


class DomainFilter(FilterSet):
    class Meta:
        model = Domain
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all().order_by("id")
    filter_class = DomainFilter
    serializer_class = DomainSerializer