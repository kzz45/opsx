from django.db import models
from django.db.models import Q
from dops.models import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from django.contrib.auth.models import User


class UserStandardRole(BaseModel):
    class Meta:
        verbose_name_plural = "标准用户角色"
    name = models.CharField(max_length=255, verbose_name="角色名称", unique=True)
    desc = models.CharField(max_length=255, verbose_name="角色描述", null=True)

    def __str__(self):
        return self.name


class UserStandardRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStandardRole
        fields = "__all__"


class UserStandardRoleFilter(FilterSet):
    class Meta:
        model = UserStandardRole
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class UserStandardRoleViewSet(viewsets.ModelViewSet):
    queryset = UserStandardRole.objects.all().order_by("-id")
    filter_class = UserStandardRoleFilter
    serializer_class = UserStandardRoleSerializer