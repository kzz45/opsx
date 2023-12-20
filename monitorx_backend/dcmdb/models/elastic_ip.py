
from django.db import models
from dops.models import BaseModel
from dcmdb.models.machine import Machine
from dcmdb.models.factory import Factory
from dcmdb.models.domain_record import DomainRecord
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class ElasticIP(BaseModel):
    name = models.CharField(max_length=255, verbose_name="名称", default='', blank=True, null=True)
    external_uuid = models.CharField(max_length=255, verbose_name="外部ID", default="",unique=True)
    version = models.CharField(max_length=255, verbose_name="版本", default='')
    state = models.CharField(max_length=255, verbose_name="状态", default='')
    public_ip = models.CharField(max_length=255, verbose_name="弹性IP")
    bind_type = models.CharField(max_length=255, verbose_name="关联资源类型", null=True)
    bind_id = models.CharField(max_length=255, verbose_name="关联资源ID", null=True)
    # domain = models.ForeignKey(to=DomainRecord, on_delete=models.CASCADE, verbose_name="IP关联的域名", null=True, blank=True)
    # machine = models.ForeignKey(to=Machine, on_delete=models.CASCADE, verbose_name="IP关联的主机", null=True, blank=True)
    factory = models.ForeignKey(to=Factory, on_delete=models.CASCADE, verbose_name="关联云厂商", blank=True, null=True)

    def __str__(self):
        return self.public_ip


class ElasticIPSerializer(serializers.ModelSerializer):
    factory__name = serializers.CharField(source="factory.name", read_only=True)

    class Meta:
        model = ElasticIP
        fields = "__all__"


class ElasticIPFilter(FilterSet):
    class Meta:
        model = ElasticIP
        fields = {
            "id": ["exact", "in"],
            "external_uuid": ["exact", "in", "contains"],
            "name": ["exact", "in", "contains"],
            "version": ["exact", "in", "contains"],
            "state": ["exact", "in", "contains"],
            "public_ip": ["exact", "in", "contains"],
            "factory__name": ["exact", "in", "contains", "startswith"],
            "bind_id": ["exact", "in", "contains"],
        }


class ElasticIPViewSet(viewsets.ModelViewSet):
    queryset = ElasticIP.objects.all().order_by("id")
    filter_class = ElasticIPFilter
    serializer_class = ElasticIPSerializer
