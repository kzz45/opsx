import json
import time
from django.db import models
from django.db.models import Q
from rest_framework.decorators import action
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from public.models.product import Product
from django.contrib.auth.models import User


class Silence(BaseModel):
    class Meta:
        verbose_name_plural = "告警维护"

    uuid = models.CharField(max_length=255, verbose_name="维护ID", null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="策略名称", null=True)
    is_regex = models.IntegerField(default=0, verbose_name="是否正则")  # 1 =~ 0 =
    match = models.TextField(verbose_name="匹配规则", null=True)
    describe = models.TextField(verbose_name="策略描述", default="")
    start = models.IntegerField(verbose_name="开始时间", default=0)
    end = models.IntegerField(verbose_name="结束时间", default=0)
    duration = models.IntegerField(verbose_name="耗时", default=0)
    unit = models.CharField(max_length=255, default="s", verbose_name="时间单位")
    state = models.IntegerField(default=1, verbose_name="状态")  # 1 生效 0 失效
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品", null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="添加者", null=True)

    def __str__(self):
        return self.name


class SilenceSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)
    user__username = serializers.CharField(source="user.username", read_only=True)
    user__first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = Silence
        fields = "__all__"


class SilenceFilter(FilterSet):
    class Meta:
        model = Silence
        fields = {
            "id": ["exact", "in"],
            "state": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class SilenceViewSet(viewsets.ModelViewSet):
    queryset = Silence.objects.all().order_by("id")
    filter_class = SilenceFilter
    serializer_class = SilenceSerializer

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(Q(user__id=self.request.user.id))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        silence_obj = serializer.save()
        silence_obj.user = self.request.user
        silence_obj.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        Silence.objects.filter(end__lt=int(time.time())).update(state=0)
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["GET"])
    def get_silences(self, request):
        data = []
        Silence.objects.filter(state=1).filter(end__lt=int(time.time())).update(state=0)
        for silence in Silence.objects.filter(state=1).filter(end__gt=int(time.time())).all():
            if silence.is_regex == 1:
                matchers_tmp = json.loads(silence.match)
                matchers = []
                for match in matchers_tmp:
                    matchers.append({
                        "name": match["name"],
                        "value": str(match["value"]),
                        "isRegex": True,
                        "isEqual": True,
                    })
            else:
                matchers_tmp = json.loads(silence.match)
                matchers = []
                for match in matchers_tmp:
                    matchers.append({
                        "name": match["name"],
                        "value": str(match["value"]),
                        "isRegex": False,
                        "isEqual": True,
                    })
            matchers.append({
                "name": "_product_id",
                "value": str(silence.product.id),
                "isRegex": False,
                "isEqual": True,
            })
            silence_dict = {
                "id": silence.id,
                "uuid": silence.uuid,
                "createdBy": silence.user.username,
                "startsAt": silence.start,
                "endsAt": silence.end,
                "comment": silence.describe,
                "matchers": matchers
            }
            data.append(silence_dict)
        return Response({"data": data})
