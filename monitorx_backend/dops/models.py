import time
from django.db import models
from django.db.models import Q
from rest_framework.response import Response
from django_filters.rest_framework import FilterSet
from rest_framework import serializers, viewsets, status
from django.contrib.auth.models import User, Group, Permission


def now_ts():
    return int(time.time())


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.AutoField(primary_key=True, unique=True)
    create_at = models.IntegerField(default=now_ts, verbose_name="创建时间")
    update_at = models.IntegerField(default=now_ts, verbose_name="更新时间")

    def save(self, *args, **kwargs):
        self.update_at = now_ts()
        super(BaseModel, self).save(*args, **kwargs)


class PermissionFilter(FilterSet):
    class Meta:
        model = Permission
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class PermissionViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Permission.objects.all().order_by("id")
    filter_class = PermissionFilter
    serializer_class = PermissionSerializer


class UserGroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = "__all__"


class UserGroupFilter(FilterSet):
    class Meta:
        model = Group
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            "id": ["exact", "in"],
            "is_active": ["exact", "in"],
            "is_superuser": ["exact", "in"],
            "username": ["exact", "contains", "in"],
            "first_name": ["exact", "contains", "in"],
        }


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField(read_only=True)
    groups = UserGroupSerializer(many=True, read_only=True)

    def get_roles(self, obj):
        result = []
        if obj.is_superuser:
            result.append("admin")
        else:
            result.append("viewer")
        return result

    class Meta:
        model = User
        fields = ["id", "is_superuser", "username", "first_name",
                  "is_active", "email", "password", "groups", "roles"]


class UserGroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("id")
    filter_class = UserGroupFilter
    serializer_class = UserGroupSerializer

    def update(self, request, *args, **kwargs):
        # 只有超管可以更新
        if not self.request.user.is_superuser:
            msg = {"status": False, "msg": "你没有权限"}
            return Response(data=msg, status=status.HTTP_403_FORBIDDEN)
        permissions = request.data.get("permissions", None)
        group_obj = self.get_object()
        group_obj.permissions.set(permissions)
        return super().update(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(~Q(username='admin')).filter(
        ~Q(username='AnonymousUser')).all().order_by('id')
    filter_class = UserFilter
    serializer_class = UserSerializer
    permission_classes = []

    def update(self, request, *args, **kwargs):
        groups = request.data.get("groups", None)
        user_obj = self.get_object()
        user_obj.groups.clear()
        user_obj.groups.add(groups)
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        groups = request.data.get("groups", None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group_obj = Group.objects.get(id=groups)
        user_obj = serializer.save()
        user_obj.groups.add(group_obj)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
