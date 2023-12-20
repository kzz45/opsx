import json
from django.db import models
from dcmdb.models.operator import Operator
from dcmdb.models.park import Park
from dcmdb.models.building import Building
from dops.models import BaseModel
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import FilterSet
from dcmdb.models.history import History


class ExportIP(BaseModel):
    cidr = models.CharField(max_length=255, verbose_name="CIRD")
    desc = models.CharField(max_length=255, verbose_name="描述", null=True)
    used = models.BooleanField(default=True, verbose_name="是否使用")
    release = models.BooleanField(default=False, verbose_name="是否释放")
    park = models.ForeignKey(to=Park, on_delete=models.CASCADE, related_name="park", verbose_name="园区", null=True)
    building = models.ForeignKey(to=Building, on_delete=models.CASCADE, verbose_name="", null=True)
    operator = models.ForeignKey(to=Operator, on_delete=models.CASCADE, verbose_name="运营商", null=True)

    def __str__(self):
        return self.cidr


class ExportIPSerializer(serializers.ModelSerializer):
    park__name = serializers.CharField(source="park.name", read_only=True)
    building__name = serializers.CharField(source="building.name", read_only=True)
    operator__name = serializers.CharField(source="operator.name", read_only=True)

    class Meta:
        model = ExportIP
        fields = "__all__"


class ExportIPFilter(FilterSet):
    class Meta:
        model = ExportIP
        fields = {
            "id": ["exact", "in"],
            "cidr": ["exact", "in", "contains"],
            "desc": ["exact", "in", "contains"],
            "park__name": ["exact", "in", "contains"],
            "operator__name": ["exact", "in", "contains"],
            "used": ["exact", "in"],
        }


class ExportIPViewSet(viewsets.ModelViewSet):
    queryset = ExportIP.objects.all().order_by("id")
    filter_class = ExportIPFilter
    serializer_class = ExportIPSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        content = [{"from": "null", "to": serializer.data["cidr"], "park": serializer.data["park__name"]}]
        History.objects.create(user=user, action="create", content=json.dumps(content), model="exporte_ip")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        last_instance = instance.cidr
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        content = [{"from": last_instance, "to": serializer.data["cidr"], "park": serializer.data["park__name"]}]
        History.objects.create(user=user, action="update", content=json.dumps(content), model="exporte_ip")
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        last_instance = instance.cidr
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_destroy(instance)
        content = [{"from": last_instance, "to": "null", "park": serializer.data["park__name"]}]
        History.objects.create(user=user, action="delete", content=json.dumps(content), model="exporte_ip")
        return Response(status=status.HTTP_204_NO_CONTENT)
