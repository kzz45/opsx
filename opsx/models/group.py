from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import FilterSet
from django.contrib.auth.models import Group
from opsx.models.perm import PermissionSerializer


class GroupFilter(FilterSet):
    class Meta:
        model = Group
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = "__all__"


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-id')
    filter_class = GroupFilter
    serializer_class = GroupSerializer

    def update(self, request, *args, **kwargs):
        # 只有超管可以更新
        if not self.request.user.is_superuser:
            msg = {"status": False, "msg": "你没有权限"}
            return Response(data=msg, status=status.HTTP_403_FORBIDDEN)
        permissions = request.data.get("permissions", None)
        group_obj = self.get_object()
        group_obj.permissions.set(permissions)
        return super().update(request, *args, **kwargs)
