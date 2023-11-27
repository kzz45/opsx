from django.db import models
from monitor.models.base import BaseModel
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers


class Tmpl(BaseModel):
    class Meta:
        verbose_name_plural = "模板文件"

    mode_choices = ((0, "通知模版"), (1, "Prom模板"), (2, "Alert模板"), (3, "实例模板"))

    name = models.CharField(max_length=255, verbose_name="名称")
    mode = models.IntegerField(verbose_name="类型", choices=mode_choices, default=0)
    content = models.TextField(verbose_name="内容")

    def __str__(self):
        return self.name


class TmplSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tmpl
        fields = "__all__"


class TmplFilter(FilterSet):
    class Meta:
        model = Tmpl
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
        }


class TmplViewSet(viewsets.ModelViewSet):
    queryset = Tmpl.objects.all().order_by("id")
    filter_class = TmplFilter
    serializer_class = TmplSerializer
