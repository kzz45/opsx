import json
from django.db import models
from dmonitor.models.base import BaseModel
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet
from django.contrib.auth import get_user_model
User = get_user_model()


class AdCident(BaseModel):
    name = models.CharField(max_length=255, verbose_name="事故名称")
    start_time = models.IntegerField(default=0, verbose_name="发生时间")
    recover_time = models.IntegerField(default=0, verbose_name="恢复时间")
    duration = models.IntegerField(default=0, verbose_name="耗时")
    status = models.IntegerField(default=0, verbose_name="事故状态")  # 1: 已解决 2: 待解决 3: 处理中
    scope = models.TextField(verbose_name="事故影响范围", blank=True)
    level = models.IntegerField(default=0, verbose_name="事故等级")  # 0 1 2 3 4 5
    # user = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name="负责人", null=True)
    people = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name="负责人", null=True)
    reason = models.TextField(verbose_name="事故原因", blank=True)
    solution = models.TextField(verbose_name="解决方式", blank=True)
    process = models.TextField(default=json.dumps([]), verbose_name="处理过程", blank=True)
    plan = models.TextField(default=json.dumps([]), verbose_name="后续规避方案", blank=True)

    def __str__(self):
        return self.name


class AdCidentSerializer(serializers.ModelSerializer):
    user__first_name = serializers.CharField(source="people.first_name", read_only=True)
    duration = serializers.SerializerMethodField(read_only=True)

    def get_duration(self, obj):
        return obj.recover_time - obj.start_time

    def validate_duration(self):
        if self.initial_data['recover_time']:
            return self.initial_data['recover_time'] - self.initial_data['start_time']
        else:
            return 0

    class Meta:
        model = AdCident
        fields = "__all__"


class AdCidentFilter(FilterSet):
    class Meta:
        model = AdCident
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class AdCidentViewSet(viewsets.ModelViewSet):
    queryset = AdCident.objects.all().order_by("id")
    filter_class = AdCidentFilter
    serializer_class = AdCidentSerializer
