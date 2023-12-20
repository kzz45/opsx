# 接收告警的用户组

from django.db import models
from dmonitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework.response import Response
from rest_framework import viewsets, serializers, status
from django.contrib.auth import get_user_model
User = get_user_model()


class UserGroup(BaseModel):
    name = models.CharField(max_length=255, verbose_name='用户组名称')
    users = models.ManyToManyField(to=User, related_name="ug_users", default=None)
    channel = models.CharField(max_length=255, verbose_name="通知渠道", default="wechat")
    webhook = models.CharField(max_length=255, verbose_name="webhook地址", default=None, null=True)

    def __str__(self):
        return self.name


class UserGroupSerializer(serializers.ModelSerializer):
    user_list = serializers.SerializerMethodField(read_only=True)

    def get_user_list(self, ins):
        return [{'username': u.username, 'id': u.id, 'first_name': u.first_name} for u in ins.users.all()]

    class Meta:
        model = UserGroup
        fields = '__all__'


class UserGroupFilter(FilterSet):
    class Meta:
        model = UserGroup
        fields = {
            'id': ['exact', 'in'],
            'name': ['exact', 'in', 'contains']
        }


class UserGroupViewSet(viewsets.ModelViewSet):
    queryset = UserGroup.objects.all().order_by("id")
    filter_class = UserGroupFilter
    serializer_class = UserGroupSerializer

    # def create(self, request, *args, **kwargs):
    #     users = request.data.get("users", None)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user_objs = User.objects.filter(id__in=users)
    #     user_group_obj = UserGroup(name=serializer.data["name"])
    #     user_group_obj.save()
    #     user_group_obj.users.add(*user_objs)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
