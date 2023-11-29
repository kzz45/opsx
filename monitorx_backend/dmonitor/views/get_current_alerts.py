# 获取当前告警
from django.db.models import Q
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from dmonitor.models.instance_type import InstanceType
from dmonitor.models.current_alert import CurrentAlert, CurrentAlertSerializer


class GetCurrentAlert(APIView):
    permission_classes = []

    def get(self, request, formt=None):
        TYPE_MAP = {i.value: i.name for i in InstanceType.objects.all()}
        data = []
        data = CurrentAlert.objects.values('product__name', 'product__id').annotate(count=Count('id'))
        for product in data:
            product['instance_type'] = []
            level_count = CurrentAlert.objects.filter(
                product_id=product['product__id']).values('level').annotate(
                count=Count('id'))
            product['count'] = level_count
            instance_type_count = CurrentAlert.objects.filter(
                product_id=product['product__id']).values('instance_type').annotate(count=Count('id'))

            for instance_type in instance_type_count:
                data_tmp = {
                    'instances': [],
                    'instance_type__name': TYPE_MAP[instance_type['instance_type']],
                    'instance_type__value': instance_type['instance_type'],
                    'count': CurrentAlert.objects.filter(
                        product_id=product['product__id']).filter(
                            instance_type=instance_type['instance_type']).values('level').annotate(
                        count=Count('id'))
                }
                instances = CurrentAlert.objects.filter(
                    product_id=product['product__id']).filter(
                        instance_type=instance_type['instance_type']).values('instance_name', 'endpoint').annotate(
                    count=Count('id'))
                data_tmp['instances'] = instances
                for instance in data_tmp['instances']:
                    instance['count'] = CurrentAlert.objects.filter(
                        product_id=product['product__id']).filter(
                            instance_type=instance_type['instance_type']).filter(
                                instance_name=instance['instance_name']).values('level').annotate(
                        count=Count('id'))
                    instance['alerts'] = CurrentAlertSerializer(CurrentAlert.objects.filter(
                        product_id=product['product__id']).filter(
                            instance_type=instance_type['instance_type']).filter(
                                instance_name=instance['instance_name']).all(), many=True).data
                product['instance_type'].append(data_tmp)

        return Response(data)
