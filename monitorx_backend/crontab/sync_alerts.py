# -*- coding: utf-8 -*-

import os
os.environ.update({"DJANGO_SETTINGS_MODULE": "dops.settings"})
import django
django.setup()
from django.conf import settings
from django.core.cache import cache

import json
import arrow
from dmonitor.models.alert import Alert
from django_redis import get_redis_connection
conn = get_redis_connection("monitor")


def sync_alerts():
    msg = json.loads(conn.blpop("endpoints")[1].decode('utf-8'))
    # print(msg)
    labels = msg['labels']
    alert_name = labels['alertname']
    instance_type = labels.get('_type', '-')
    instance_name = labels.get('_name', '-')
    ip = labels.get('_ip', '-')
    product_id = int(labels.get('_product_id', -1))
    if product_id == 0:
        product_id = -1

    endpoint = labels.get('_endpoint', '-')
    level = labels.get('level', '-')
    state = msg['status']
    summary = msg['annotations']['summary']
    description = msg['annotations']['description']
    start = arrow.get(msg['startsAt']).timestamp()
    end = arrow.get(msg['endsAt']).timestamp()
    # print(msg)
    new_alert = Alert(name=alert_name,
                      instance_type=instance_type,
                      instance_name=instance_name,
                      ipaddr=ip,
                      product_id=product_id,
                      endpoint=endpoint,
                      level=level,
                      state=state,
                      labels=json.dumps(labels),
                      summary=summary,
                      description=description,
                      start=start,
                      end=0)
    if state == 'firing':
        print('firing')
        new_alert.save()
    if state == 'resolved':
        print('resolved')
        alert = Alert.objects.filter(name=alert_name)\
            .filter(instance_type=instance_type)\
            .filter(instance_name=instance_name)\
            .filter(ipaddr=ip)\
            .filter(product_id=product_id)\
            .filter(endpoint=endpoint)\
            .filter(level=level)\
            .filter(start=start).first()
        if alert:
            alert.state = 'resolved'
            alert.end = end
            alert.save()
        else:
            new_alert.end = end
            new_alert.save()


sync_alerts()
