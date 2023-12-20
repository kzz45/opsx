from django.db import models
from django.db.models import Q
from dops.models import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from django.contrib.auth.models import User


class UserGroup(BaseModel):
    class Meta:
        verbose_name_plural = "用户分组"

    name = models.CharField(max_length=255, verbose_name="用户组名称")
    desc = models.CharField(max_length=255, verbose_name="用户组描述", null=True)
    admin = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="ugadmin", verbose_name="管理员")
    # users = models.ManyToManyField(to=User, related_name="usergroup", verbose_name="成员")
    # role = models.ManyToManyField(to=UserStandardRole, related_name="role", verbose_name="角色")

    def __str__(self):
        return self.name


class UserGroupSerializer(serializers.ModelSerializer):
    admin__username = serializers.CharField(source="admin.username", read_only=True)
    admin__first_name = serializers.CharField(source="admin.first_name", read_only=True)
    # role__name = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = UserGroup
        fields = '__all__'


class UserGroupFilter(FilterSet):
    class Meta:
        model = UserGroup
        fields = {
            'id': ['exact', 'in'],
            'name': ['exact', 'in', 'contains'],
        }


class UserGroupViewSet(viewsets.ModelViewSet):
    queryset = UserGroup.objects.all().order_by("id")
    filter_class = UserGroupFilter
    serializer_class = UserGroupSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def create(self, request, *args, **kwargs):
        # 只有超管可以创建
        if not self.request.user.is_superuser:
            msg = {"status": False, "msg": "你没有权限"}
            return Response(data=msg, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        # 只有超管或者管理员可以更新
        queryset = self.get_queryset().filter(id=pk).filter(Q(admin__id=self.request.user.id))
        if self.request.user.is_superuser or queryset:
            return super().update(request, *args, **kwargs)
        else:
            msg = {"status": False, "msg": "你没有权限"}
            return Response(data=msg, status=status.HTTP_403_FORBIDDEN)
