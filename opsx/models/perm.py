from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet
from django.contrib.auth.models import Permission


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
    queryset = Permission.objects.all().order_by("-id")
    filter_class = PermissionFilter
    serializer_class = PermissionSerializer