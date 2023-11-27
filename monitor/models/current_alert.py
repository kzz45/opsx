from django.db import models
from django.db.models import Q
from django.db.models import Count
from monitor.models.base import BaseModel
from rest_framework.decorators import action
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from public.models.product import Product
from monitor.models.instance_type import InstanceType


class CurrentAlert(BaseModel):
    class Meta:
        verbose_name_plural = "当前告警"

    job = models.CharField(max_length=255, verbose_name="监控任务")
    name = models.CharField(max_length=255, verbose_name="告警名称")
    fingerprint = models.CharField(max_length=255, verbose_name="指纹")
    instance_type = models.CharField(max_length=255, verbose_name="实例类型")
    instance_name = models.CharField(max_length=255, verbose_name="实例名称")
    ipaddr = models.CharField(max_length=255, verbose_name="IP地址")
    endpoint = models.CharField(max_length=255, verbose_name="Endpoint")
    level = models.CharField(max_length=36, verbose_name="级别")
    state = models.CharField(max_length=36, verbose_name="状态")
    receivers = models.CharField(max_length=255, verbose_name="接收人")
    labels = models.TextField(verbose_name="标签")
    summary = models.TextField(verbose_name="概括")
    description = models.TextField(verbose_name="描述", null=True)
    start = models.IntegerField(verbose_name="开始时间")
    update = models.IntegerField(verbose_name="更新时间")
    value = models.FloatField(verbose_name="值")
    deleted = models.IntegerField(verbose_name="是否删除", default=0)  # 1: 删除
    deleted_ts = models.IntegerField(verbose_name="删除时间", default=0)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name="产品")

    def __str__(self):
        return self.name


class CurrentAlertSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = CurrentAlert
        fields = "__all__"


class CurrentAlertFilter(FilterSet):
    class Meta:
        model = CurrentAlert
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "product": ["exact", "in"],
        }


class CurrentAlertViewSet(viewsets.ModelViewSet):
    queryset = CurrentAlert.objects.all().order_by("name")
    filter_class = CurrentAlertFilter
    serializer_class = CurrentAlertSerializer

    @action(detail=False, methods=["GET"])
    def alert_wall(self, request):
        itmap = {i.desc: i.name for i in InstanceType.objects.all()}
        crit__product = []  # 崩盘
        warn__product = []  # 警告
        silence__product = []  # 维护

        # 告警产品
        products = CurrentAlert.objects.filter(
            deleted=0).filter(Q(product__user_group__users__id=self.request.user.id))\
            .values("product_id", "product__name")\
            .annotate(count=Count("id"))

        for product in products:
            product["statistics"] = []
            # 告警等级
            level_count = CurrentAlert.objects.filter(
                deleted=0).filter(Q(product__user_group__users__id=self.request.user.id))\
                .filter(product_id=product["product_id"])\
                .values("level").annotate(count=Count("id"))

            level_count = {i["level"]: i["count"] for i in level_count}

            product["statistics"].append({
                "name": "level",
                "display": "等级",
                "count": [
                        {"name": "crit",
                         "display": "严重",
                         "count": level_count.get("crit", 0)
                         },
                        {"name": "warn",
                         "display": "警告",
                         "count": level_count.get("warn", 0)
                         },
                        {"name": "info",
                         "display": "处理",
                         "count": 0
                         }
                ]
            })
            # 告警名称
            alertname_count = CurrentAlert.objects.filter(
                deleted=0).filter(Q(product__user_group__users__id=self.request.user.id))\
                .filter(product_id=product["product_id"])\
                .values("name").annotate(count=Count("id"))

            product["statistics"].append({
                "name": "alertname",
                "display": "报警名称",
                "count": [{"name": i["name"], "display":i["name"], "count":i["count"]} for i in alertname_count]
            })

            # 告警类型
            instance_type_count = CurrentAlert.objects.filter(
                deleted=0).filter(Q(product__user_group__users__id=self.request.user.id))\
                .filter(product_id=product['product_id'])\
                .values('instance_type')\
                .annotate(count=Count('id'))
            product['statistics'].append({
                'name': 'type',
                'display': '类型',
                'count': [{'name': i['instance_type'], 'display':itmap.get(i['instance_type'], '未知'), 'count':i['count']} for i in instance_type_count]
            })

            product['status'] = 'monitor'
            if product['statistics'][0]['count'][0]['count'] > 0:
                crit__product.append(product)
            elif product['statistics'][0]['count'][1]['count'] > 0:
                warn__product.append(product)
            else:
                silence__product.append(product)
                product['status'] = 'silence'
            # print("=" * 20, product)
        products = crit__product + warn__product + silence__product
        return Response(data=products)
