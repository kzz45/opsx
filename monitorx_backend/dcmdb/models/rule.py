from django.db import models
from dops.models import BaseModel
from dcmdb.models.security import Security
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet


class Rule(BaseModel):
    name = models.CharField(max_length=255, verbose_name="安全组规则名称", null=True, blank=True)
    rule_id = models.CharField(max_length=255, verbose_name="安全组规则ID", null=True, blank=True)
    security = models.ForeignKey(to=Security, on_delete=models.PROTECT, verbose_name="安全组", null=True)
    policy = models.CharField(max_length=255, verbose_name="安全组策略(允许/拒绝)", null=True)
    direction = models.CharField(max_length=255, verbose_name="规则类型(出站/入站)", null=True)
    protocol = models.CharField(max_length=255, verbose_name="协议", null=True)
    priority = models.IntegerField(verbose_name="优先级", null=True)
    ip = models.TextField(verbose_name="ip", null=True)
    port = models.CharField(max_length=255, verbose_name="端口", null=True)

    def __str__(self):
        return self.rule_id

    class Meta:
        verbose_name_plural = "安全组规则"


class RuleSerializer(serializers.ModelSerializer):
    security__security_id = serializers.CharField(source="security.security_id", read_only=True)

    class Meta:
        model = Rule
        fields = "__all__"


class RuleFilter(FilterSet):
    class Meta:
        model = Rule
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "security__security_id": ["exact", "in"],
            "policy": ["exact", "in"],
            "direction": ["exact", "in"],
            "protocol": ["exact", "in"],
            "priority": ["exact", "in"],
            "ip": ["exact", "in"],
            "port": ["exact", "in"],
            "rule_id": ["exact", "in"],
        }


class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all().order_by("id")
    filter_class = RuleFilter
    serializer_class = RuleSerializer
