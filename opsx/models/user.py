from django.db.models import Q
from rest_framework.response import Response
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from django_filters.rest_framework import FilterSet
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from opsx.models.group import GroupSerializer
from public.models.user_group import UserGroup


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
    groups = GroupSerializer(many=True, read_only=True)

    def get_roles(self, obj):
        result = []
        if obj.is_superuser:
            result.append("admin")
        else:
            result.append("viewer")
        return result

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "password",
                  "email", "is_superuser", "is_active", "groups", "roles"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(~Q(username="admin")).filter(
        ~Q(username="AnonymousUser")).all().order_by("-id")
    filter_class = UserFilter
    serializer_class = UserSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        # 如果一个用户是一个用户组的管理员, 则也可以
        if UserGroup.objects.filter(admin=self.request.user.id).exists():
            return queryset
        return queryset.filter(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        # 只有管理员可以
        if self.request.user.is_superuser:
            groups = request.data.get("groups", None)
            user_obj = self.get_object()
            user_obj.groups.clear()
            user_obj.groups.add(groups)
            return super().update(request, *args, **kwargs)
        else:
            msg = {"status": False, "msg": "你没有权限"}
            return Response(data=msg, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        groups = request.data.get("groups", None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group_obj = Group.objects.get(id=groups)
        user_obj = serializer.save()
        user_obj.groups.add(group_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 登录
    @action(detail=False, methods=["POST"])
    def login(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

    # 登出
    @action(detail=False, methods=["POST"])
    def logout(self, request):
        pass
