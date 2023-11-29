# -*- coding: utf-8 -*-

import os
import sys
WORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(WORK_DIR)
import django
os.environ.update({"DJANGO_SETTINGS_MODULE": "dops.settings"})
django.setup()
from django.conf import settings
from django.core.cache import cache

import time
import json
import arrow
import requests
from urllib import parse
from urllib.parse import parse_qs, urlparse
from dmonitor.models.task import Task
from dmonitor.models.addon import AddOn
from dmonitor.models.label import Label
from dmonitor.models.alert import Alert
from dcmdb.models.machine import Machine
from dcmdb.models.product import Product
from dmonitor.models.server import Server
from dmonitor.models.instance import Instance
from dmonitor.models.alert_route import AlertRoute
from dmonitor.models.current_alert import CurrentAlert
from dmonitor.models.server_group import ServerGroup
from django_redis import get_redis_connection
conn = get_redis_connection("monitor")


# 获取维护列表
def get_silences():
    silence_map = {}
    resp = requests.get('http://127.0.0.1:9093/api/v2/silences?silenced=false&inhibited=false', verify=False)
    for i in resp.json():
        if i['status']['state'] == 'expired':
            continue
        silence_map[i['id']] = i['createdBy']
    return silence_map


# 全部的告警列表
def get_alerts():
    #resp = requests.get(settings.ALERTMANAGER + '/api/v2/alerts?silenced=true&inhibited=false', verify=False)
    resp = requests.get('http://127.0.0.1:9093/api/v2/alerts?silenced=true&inhibited=false', verify=False)
    data = resp.json()
    return data


# 当前实时告警
def sync_current_alert():
    current_alerts = []
    # resp = requests.get(settings.ALERTMANAGER + '/api/v2/alerts?silenced=true&inhibited=false')
    alerts = get_alerts()
    silence_map = get_silences()
    #print("-" * 20, silence_map)
    alertmanager_alerts_set = set([alert['fingerprint'] for alert in alerts])
    local_db_alerts_set = set([alert.fingerprint for alert in CurrentAlert.objects.all()])
    need_add_alerts = alertmanager_alerts_set - local_db_alerts_set
    need_delete_alerts = local_db_alerts_set - alertmanager_alerts_set
    now_ts = int(time.time())
    product_ids = set([i.id for i in Product.objects.all()])
    # 需要删除的，标记为删除
    CurrentAlert.objects.filter(deleted=0).filter(
        fingerprint__in=list(need_delete_alerts)).update(deleted=1, deleted_ts=now_ts)
    # 之前标记删除 又重新报警的，重置删除状态
    CurrentAlert.objects.filter(deleted=1).filter(
        fingerprint__in=list(alertmanager_alerts_set)).update(deleted=0, deleted_ts=0)
    # 清理标记删除超过30分钟的报警
    CurrentAlert.objects.filter(deleted=1).filter(
        deleted_ts__lt=now_ts - 1800).delete()

    ps = []
    for alert in alerts:
        fingerprint = alert['fingerprint']
        silence = silence_map.get(alert['status']['silencedBy'][0], None) if alert['status']['silencedBy'] else None
        #print("+" * 20, silence)
        if silence:
            silence = int(silence)
        # 如果是不需要添加的，判断此报警是否被维护
        if fingerprint not in need_add_alerts:
            ca = CurrentAlert.objects.filter(fingerprint=fingerprint).first()
            if ca.silence != silence:
                ca.silence_id = silence
                ca.save()
        else:
            labels = alert['labels']
            name = labels['alertname']
            instance_type = labels.get('_type', '-')
            job = labels.get('job', '-')
            instance_name = labels.get('_name', '-')
            ipaddr = labels.get('_ip', '-')
            product_id = int(labels.get('_product_id', -1))
            ps.append(product_id)
            if product_id not in product_ids:
                continue
            endpoint = labels.get('_endpoint', '-')

            level = labels.get('level', '-')
            state = alert['status']['state']
            silence = silence_map.get(alert['status']['silencedBy'][0], None) if alert['status']['silencedBy'] else None
            receivers = ','.join([i['name'] for i in alert['receivers']])
            # if product_id == -1:
            #     task = Task.objects.filter(name=job).first()
            #     if task:
            #         ip = endpoint
            #         product_id = task.product.id
            #         ar = AlertRoute.objects.filter(product__id=product_id).filter(parent=0).first()
            #         receivers = ar.receiver.first().id
            graph = parse.parse_qs(parse.urlsplit(alert['generatorURL']).query)['g0.expr'][0]
            summary = alert['annotations']['summary']
            description = alert['annotations']['description']
            start = arrow.get(alert['startsAt']).timestamp()
            update = arrow.get(alert['updatedAt']).timestamp()
            value = alert['annotations'].get('value', 0)
            if type(value) == str:
                value = 0
            current_alerts.append(
                CurrentAlert(
                    name=name,
                    fingerprint=fingerprint,
                    job=job,
                    instance_type=instance_type,
                    instance_name=instance_name,
                    ipaddr=ipaddr,
                    product_id=product_id,
                    endpoint=endpoint,
                    level=level,
                    state=state,
                    silence=silence,
                    # silence=None,
                    receivers=receivers,
                    graph=graph,
                    summary=summary,
                    description=description,
                    start=start,
                    update=update,
                    value=value,
                    labels=json.dumps(labels, ensure_ascii=False)
                )
            )

    CurrentAlert.objects.bulk_create(current_alerts)


sync_current_alert()
