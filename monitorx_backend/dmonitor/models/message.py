
from django.db import models
from dmonitor.models.base import BaseModel
from dcmdb.models.product import Product
from rest_framework import serializers, viewsets
from django_filters.rest_framework import FilterSet
from django.contrib.auth import get_user_model
User = get_user_model()


class Message(BaseModel):
    name = models.CharField(max_length=255, verbose_name="消息名称")
    instance_name = models.CharField(max_length=255, default='-', verbose_name="实例名称")
    ipaddr = models.CharField(max_length=255, verbose_name="IP地址", null=True)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品")
    endpoint = models.CharField(max_length=255, verbose_name="端点")
    level = models.CharField(max_length=255, verbose_name="级别")
    state = models.CharField(max_length=255, verbose_name="状态")
    summary = models.TextField(default='', verbose_name="概括", blank=True)
    description = models.TextField(default='', verbose_name="描述", blank=True)
    time = models.IntegerField(verbose_name="发生时间")
    merge_num = models.IntegerField(verbose_name="聚合数量", default=None)
    users = models.ManyToManyField(to=User, related_name="msg_users", verbose_name="用户", blank=True)

    def __str__(self):
        return self.name


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MessageFilter(FilterSet):
    class Meta:
        model = Message
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by("id")
    filter_class = MessageFilter
    serializer_class = MessageSerializer
