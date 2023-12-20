from django.db import models
from dcmdb.models.role import UserStandardRole
from dcmdb.models.user_group import UserGroup
from dops.models import BaseModel
from django.contrib.auth.models import User
from rest_framework import viewsets, serializers, status
from django_filters.rest_framework import FilterSet


class UserRoleGroup(BaseModel):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name="成员")
    group = models.ForeignKey(
        to=UserGroup, on_delete=models.CASCADE, verbose_name="用户组")
    role = models.ForeignKey(
        to=UserStandardRole, on_delete=models.CASCADE, verbose_name="角色")


class UserRoleGroupSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.first_name", read_only=True)
    group__name = serializers.CharField(source="group.name", read_only=True)
    role__name = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = UserRoleGroup
        fields = "__all__"


class UserRoleGroupFilter(FilterSet):
    class Meta:
        model = UserRoleGroup
        fields = {
            "user_id": ["exact", "in"],
            "group_id": ["exact", "in"],
            "role_id": ["exact", "in"],
        }


class UserRoleGroupViewSet(viewsets.ModelViewSet):
    queryset = UserRoleGroup.objects.all().order_by("-id")
    filter_class = UserRoleGroupFilter
    serializer_class = UserRoleGroupSerializer
    permission_classes = []
