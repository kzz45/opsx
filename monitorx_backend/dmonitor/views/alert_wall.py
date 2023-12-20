import json
from django.db.models import Q
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from dmonitor.models.instance_type import InstanceType
from dmonitor.models.current_alert import CurrentAlert


class AlertWall(APIView):
    permission_classes = []

    def get(self, request):
        data = []
        itmap = {i.value: i.name for i in InstanceType.objects.all()}
        by_product = request.query_params.get('by_product')
        self_health = request.query_params.get('self_health', 0)
        product__id = request.query_params.get('product__id', None)
        crit__product = []  # 崩盘
        warn__product = []  # 警告
        ticket__product = []  # 事故
        silence__product = []  # 维护
        if by_product:
            if product__id:
                products = CurrentAlert.objects.filter(deleted=0).filter(product_id=product__id).values('product_id', 'product__name').annotate(count=Count('id'))
            else:
                products = CurrentAlert.objects.filter(deleted=0).values('product_id', 'product__name').annotate(count=Count('id'))
            for product in products:
                product['statistics'] = []
                level_count = CurrentAlert.objects.filter(deleted=0).filter(product_id=product['product_id']).filter(silence__isnull=True).filter(ticket__isnull=True).filter(checked=0).values('level').annotate(
                    count=Count('id'))

                level_count = {i['level']: i['count'] for i in level_count}
                ticket_count = CurrentAlert.objects.filter(
                    product_id=product['product_id']).filter(deleted=0).filter(Q(ticket__isnull=False) | Q(checked=1)).filter(silence__isnull=True).count()
                product['statistics'].append({
                    'name': 'level',
                    'display': '等级',
                    'count': [
                        {'name': 'crit',
                         'display': '严重',
                         'count': level_count.get('crit', 0)},
                        {'name': 'warn',
                         'display': '警告',
                         'count': level_count.get('warn', 0)},
                        {'name': 'info',
                         'display': '处理',
                         'count': ticket_count},
                        {'name': 'silence',
                         'display': '维护',
                         'count': CurrentAlert.objects.filter(deleted=0).filter(product_id=product['product_id']).filter(silence__isnull=False).count()
                         }
                    ]
                })

                alertname_count = CurrentAlert.objects.filter(deleted=0).filter(product_id=product['product_id']).values('name').annotate(
                    count=Count('id'))
                product['statistics'].append({
                    'name': 'alertname',
                    'display': '报警名称',
                    'count': [{'name': i['name'], 'display':i['name'], 'count':i['count']} for i in alertname_count]
                })
                silence_count = CurrentAlert.objects.filter(deleted=0).filter(
                    product_id=product['product_id']).filter(silence__isnull=False).count()

                product['statistics'].append({
                    'name': 'silence',
                    'display': '维护状态',
                    'count': [
                        {'name': 'silence',
                         'display': '维护',
                         'count': silence_count},
                        {'name': 'ticket',
                         'display': '处理',
                         'count': ticket_count},
                        {'name': 'monitor',
                         'display': '监控',
                         'count': level_count.get('crit', 0) + level_count.get('warn', 0)},
                    ]
                })
                
                instance_type_count = CurrentAlert.objects.filter(deleted=0).filter(product_id=product['product_id']).values('instance_type').annotate(count=Count('id'))
                product['statistics'].append({'name': 'type',
                                              'display': '类型',
                                              'count': [{'name': i['instance_type'], 'display':itmap.get(i['instance_type'], '未知'), 'count':i['count']} for i in instance_type_count]
                                              })

                product['status'] = 'monitor'
                if product['statistics'][0]['count'][0]['count'] > 0:
                    crit__product.append(product)
                elif product['statistics'][0]['count'][1]['count'] > 0:
                    warn__product.append(product)
                elif product['statistics'][0]['count'][2]['count'] > 0:
                    ticket__product.append(product)
                else:
                    silence__product.append(product)
                    product['status'] = 'silence'
        products = crit__product + warn__product + ticket__product + silence__product
        return Response(products)
