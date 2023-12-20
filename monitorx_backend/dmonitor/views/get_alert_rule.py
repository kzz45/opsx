import json
from rest_framework.views import APIView
from rest_framework.response import Response
from dmonitor.models.adjust import AdJust
from dmonitor.models.alert_rule import AlertRule


class GetAlertRule(APIView):
    permission_classes = []

    def get(self, request):
        result = {
            "rules": []
        }
        alert_rule_objs = AlertRule.objects.all()
        for alert_rule in alert_rule_objs:
            result['rules'].extend(get_rules(alert_rule))
        return Response(result)


def get_rules(alert_rule):
    data = []
    adjust_objs = AdJust.objects.filter(alert_rule=alert_rule).filter(parent=1).all()
    alert_rule_dict = {
        "alert": alert_rule.name,
        "expr": alert_rule.expression,
        "for": str(alert_rule.interval) + "s",
        "labels": {"level": alert_rule.level},
        "annotations": {"summary": alert_rule.summary, "description": alert_rule.description}
    }
    # op(操作符)为空则直接返回
    if not alert_rule.op:
        data.append(alert_rule_dict)
        return data

    # 规则下面没有微调规则
    if not adjust_objs:
        alert_rule_dict['expr'] += " {} {}".format(alert_rule.op, alert_rule.value)
        data.append(alert_rule_dict)
        return data

    # 规则下面有微调规则
    exclude_matchs = [
        '{0}!="{1}",'.format(match['name'], match['value'])
        for match in [json.loads(i.match)[0] for i in adjust_objs if i.is_cover == 1]
    ]
    # print("-" * 20, exclude_matchs)
    # 通过子规则 先反推出全局的规则
    label_match = [json.loads(i.match) for i in adjust_objs if i.is_cover == 1]
    # print("+" * 20, label_match)
    # exclude_matchs = ['{0}!="{1}",'.format(match['name'], match['value']) for match in label_match[0]]
    expr = alert_rule_dict['expr']
    if exclude_matchs:
        alert_rule_dict['expr'] = expr.replace('{', '{%s' % (''.join(exclude_matchs)))
    alert_rule_dict['expr'] += " {} {}".format(alert_rule.op, alert_rule.value)
    data.append(alert_rule_dict)
    # 处理子规则
    for adjust_obj in adjust_objs:
        process_adjust(data, adjust_obj, alert_rule, alert_rule_dict)
    return data


def process_adjust(data, adjust_obj, ar, ar_dict, parent_layer=None):
    # 处理规则下的微调
    ar_dict = json.loads(json.dumps(ar_dict))
    ar_tmp = json.loads(json.dumps(ar_dict))
    # 子规则的匹配标签
    match = json.loads(adjust_obj.match)[0]
    # include_matchs = ['{0}="{1}"'.format(m['name'], m['value']) for m in match]
    # print('*' * 30, include_matchs)

    next_adjs = AdJust.objects.filter(parent=adjust_obj.id).all()
    # 如果是第一层微调
    if adjust_obj.parent == 1:
        this_layer = ar.expression.replace("}", ",%s='%s'}" % (match['name'], match['value']))
    else:
        this_layer = parent_layer + ' and ' + ar.expression.replace("}", ",%s='%s'}" % (match['name'], match['value']))
    # print('?' * 20, this_layer)
    # this_layer = ar.expression.replace("}", ",%s}" % ','.join(include_matchs))
    expr = this_layer
    # print('-' * 30, expr)
    for next_adj in next_adjs:
        if next_adj.is_cover == 1:
            next_adj_match = json.loads(next_adj.match)[0]
            expr += " and "
            expr += ar.expression.replace("}", ",%s!='%s'}" % (next_adj_match['name'], next_adj_match['value']))
    # print('0' * 30, expr)
    ar_tmp['expr'] = expr + " {} {}".format(adjust_obj.op, adjust_obj.value)
    ar_tmp['expr'] = ar_tmp['expr'].replace('{,', '{')
    ar_tmp['labels']['level'] = adjust_obj.level
    ar_tmp['labels']['alert_id'] = ar.id
    ar_tmp['labels']['adjust_id'] = adjust_obj.id
    # print("=" * 30, ar_tmp)
    data.append(ar_tmp)
    # for next_adj in next_adjs:
    #     print(next_adj)
    #     process_adjust(data, next_adj, ar, ar_dict, parent_layer=this_layer)
