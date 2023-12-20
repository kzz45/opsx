from dcmdb.models.domain import Domain
from django.db import models
from dops.models import BaseModel
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class DomainRecord(BaseModel):
    rr = models.CharField(max_length=255, verbose_name="主机记录")
    type = models.CharField(max_length=255, verbose_name="记录类型")
    value = models.CharField(max_length=255, verbose_name="记录值")
    desc = models.CharField(max_length=255, verbose_name="描述", null=True)
    status = models.CharField(max_length=255, verbose_name="状态")
    domain = models.ForeignKey(to=Domain, on_delete=models.PROTECT, verbose_name="主域名")


class DomainRecordSerializer(serializers.ModelSerializer):
    domain__name = serializers.CharField(source="domain.name", read_only=True)
    factory__name = serializers.CharField(source="domain.factory.name", read_only=True)

    def get_whole__name(self, obj):
        return obj.rr + "." + obj.domain.name

    class Meta:
        model = DomainRecord
        fields = "__all__"


class DomainRecordFilter(FilterSet):
    class Meta:
        model = DomainRecord
        fields = {
            "id": ["exact", "in"],
            "type": ["exact", "in", "contains"],
            "value": ["exact", "in", "contains"],
            "domain": ["exact", "in"],
            "domain__name": ["exact", "in", "contains"],
        }


class DomainRecordViewSet(viewsets.ModelViewSet):
    queryset = DomainRecord.objects.all().order_by("id")
    filter_class = DomainRecordFilter
    serializer_class = DomainRecordSerializer
