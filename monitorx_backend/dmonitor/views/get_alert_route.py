import json
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from dmonitor.models.alert_route import AlertRoute


class GetAlertRoute(APIView):
    permission_classes = []

    def get(self, request):
        result = {
            "routes": []
        }
        # 接收者
        receivers = []
        # 全局告警路由
        for alert_route in AlertRoute.objects.filter(product_id=-1).all():
            match = get_match(alert_route)
            receiver = '-'.join([str(i.id) for i in alert_route.receiver.all()])
            receivers.append(receiver)
            result['routes'].append({
                match['match']: {i['name']: i['value'] for i in match['label']},
                "receiver": receiver,
                "group_wait": alert_route.group_wait,
                "group_interval": alert_route.group_interval,
                "repeat_interval": alert_route.repeat_interval,
                "group_by": json.loads(alert_route.group_by),
                "continue": True,
            })
        # 非全局路由(每个产品的主路由)
        for alert_route in AlertRoute.objects.filter(~Q(product_id=-1)).filter(parent=0).all():
            match = get_match(alert_route)
            receiver = '-'.join([str(i.id) for i in alert_route.receiver.all()])
            receivers.append(receiver)
            route = {
                match['match']: {i['name']: i['value'] for i in match['label']},
                "receiver": '-'.join([str(i.id) for i in alert_route.receiver.all()]),
                "group_wait": alert_route.group_wait,
                "group_interval": alert_route.group_interval,
                "repeat_interval": alert_route.repeat_interval,
                "group_by": json.loads(alert_route.group_by),
                "continue": True,
            }
            result['routes'].append(route)
            # 子路由
            children_route = AlertRoute.objects.filter(~Q(product_id=-1)).filter(parent=alert_route.id).all()
            if children_route:
                process_children_route(route, children_route, receivers)
        # 统一处理接收者
        result['receivers'] = []
        for i in list(set(receivers)):
            result['receivers'].append({
                "name": i,
                "webhook_configs": "http://127.0.0.1:5454/api/v1/notice/"
            })
        return Response(result)


def process_children_route(route, ars, receivers):
    route['routes'] = []
    parent_match = {}
    for k, v in route["match"].items():
        parent_match[k] = v
    # print("-" * 20, parent_match)
    for ar in ars:
        receiver = '-'.join([str(i.id) for i in ar.receiver.all(
        )]) + '-' + route['receiver'] if ar.is_raise else '-'.join([str(i.id) for i in ar.receiver.all()])
        receivers.append(receiver)
        match = get_match(ar)
        next_route_match = {i['name']: i['value'] for i in match['label']}
        # print("=" * 20, next_route_match)
        this_match = next_route_match.copy()
        this_match.update(parent_match)
        # print("?" * 20, fuck)
        next_route = {
            match['match']: this_match,
            "receiver": receiver,
            "group_wait": ar.group_wait,
            "group_interval": ar.group_interval,
            "repeat_interval": ar.repeat_interval,
            "group_by": json.loads(ar.group_by),
            "continue": ar.is_raise == 1,
        }
        route['routes'].append(next_route)
        # next_ars = AlertRoute.objects.filter(~Q(product_id=-1)).filter(parent=ar.id).all()
        # if next_ars:
        # process_children_route(next_route, next_ars, receivers)


def get_match(alert_route):
    # 匹配规则
    match_tmp = json.loads(alert_route.match)
    # if match_tmp['re']:
    #     match = 'match_re'
    # else:
    # match = 'match'
    match = 'match'
    return {"match": match, "label": match_tmp['label']}
