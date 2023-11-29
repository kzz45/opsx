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

import json
from urllib.parse import parse_qs, urlparse
from dmonitor.models.task import Task
from dmonitor.models.addon import AddOn
from dmonitor.models.label import Label
from dmonitor.models.alert import Alert
from dcmdb.models.machine import Machine
from dcmdb.models.product import Product
from dmonitor.models.server import Server
from dmonitor.models.instance import Instance
from django_redis import get_redis_connection
conn = get_redis_connection("monitor")


def filter_label(name):
    if name.startswith('_has_'):
        return False
    if name.endswith('_port'):
        return False
    return True


# 生成实例上的任务
def make_instance_tasks():
    server_uuids = [i.uuid for i in Server.objects.all()]
    for server_uuid in server_uuids:
        print('-'*10, server_uuid)
        instances = Server.objects.filter(uuid=server_uuid).first().server_group.instance_set.all()
        # print("+"*10, instances)
        task_list = []
        # 基础任务
        basic_tasks = Task.objects.filter(instances__in=instances).filter(mode=0).distinct()
        for task in basic_tasks:
            if not task.task_addons.all():
                continue
            task_instances = task.instances.all() & instances.all()
            # print("="*10, task_instances)
            instance_obj_list = []
            for i in task_instances:
                print("="*10, i)
                if i.instance_type.name == "kubernetes" and i.enable == 1:
                    instance_obj = {
                        '_endpoint': i.endpoint,
                        '_ip': i.private_ip if i.use_public_ip == 0 else i.public_ip,
                        '_name': i.name,
                        'labels': dict({l.name: l.value for l in i.labels.all() if filter_label(l.name)},
                                       **{'_product_id': str(i.product.id),
                                       '_product_name': i.product.name,
                                          '_type': i.instance_type.value,
                                          '_cluster_name': i.name,
                                          '_cluster_id': i.endpoint,
                                          }),
                        'port': 2021
                    }
                    instance_obj_list.append(instance_obj)
                if i.instance_type.name == "machine" and i.enable == 1:
                    instance_obj = {
                        '_endpoint': i.endpoint,
                        '_ip': i.private_ip if i.use_public_ip == 0 else i.public_ip,
                        '_name': i.name,
                        'labels': dict({l.name: l.value for l in i.labels.all() if filter_label(l.name)},
                                       **{'_product_id': str(i.product.id),
                                       '_product_name': i.product.name,
                                          '_type': i.instance_type.value,
                                          }),
                        'port': 2021
                    }
                    instance_obj_list.append(instance_obj)
            task_obj = {
                "task_id": task.id,
                "task_name": task.name,
                "task_mode": "direct",
                "server_uuid": server_uuid,
                "addons": [],
                "instances": instance_obj_list,
            }

            for addon in task.task_addons.all():
                if addon.probe:
                    task_obj['addons'].append(
                        {
                            "task_id": task.id,
                            "task_mode": "direct",
                            'id': addon.id,
                            'name': addon.name,
                            'mode': 'proxy',
                            'probe': addon.probe.api,
                            'probe_args': addon.probe_args,
                            "metric": urlparse(addon.args).path,
                            "params": parse_qs(urlparse(addon.args).query),
                            'interval': addon.interval,
                            'timeout': addon.timeout
                        }
                    )
                else:
                    task_obj['addons'].append(
                        {
                            "task_id": task.id,
                            "task_mode": "direct",
                            'id': addon.id,
                            'name': addon.name,
                            'mode': 'direct',
                            'probe': "",
                            'scheme': addon.scheme,
                            'port': addon.port,
                            'args': addon.args,
                            "metric": urlparse(addon.args).path,
                            "params": parse_qs(urlparse(addon.args).query),
                            'interval': addon.interval,
                            'timeout': addon.timeout
                        }
                    )
            task_list.append(task_obj)
        # 业务任务
        server = Server.objects.filter(uuid=server_uuid).first()
        # print(server.server_group)
        business_task = Task.objects.filter(mode=1).filter(server_group__name=server.server_group).all()
        # print(business_task)
        for task in business_task:
            url_split = task.url.split(',')
            urlparse_obj = urlparse(url_split[0])
            if urlparse_obj.port:
                port = urlparse_obj.port
            else:
                if urlparse_obj.scheme == 'http':
                    port = 80
                else:
                    port = 443
            task_obj = {
                "task_id": task.id,
                "task_name": task.name,
                "task_mode": "direct",
                "server_uuid": server_uuid,
                "addons": [
                    {
                        "task_id": task.id,
                        "task_mode": "direct",
                        "id": task.id,
                        "name": task.name,
                        "mode": "direct",
                        'probe': urlparse_obj.netloc,
                        "scheme": urlparse_obj.scheme,
                        "port": port,
                        "args": urlparse_obj.path + urlparse_obj.query,
                        "metric": urlparse_obj.path,
                        "params": parse_qs(urlparse_obj.query),
                        "interval": task.interval,
                        "timeout": task.timeout}
                ],
                "instances": [
                    {
                        '_endpoint': urlparse(i).scheme + "://" + urlparse(i).hostname,
                        '_name': urlparse(i).hostname,
                        '_ip': urlparse(i).hostname,
                        'labels': dict({l['name']: l['value'] for l in json.loads(task.label)}, **{'_product_id': str(task.product.id), '_product_name': task.product.name, '_type': task.instance_type.value}),
                        "port": port
                    } for i in url_split
                ]
            }
            task_list.append(task_obj)
        result = json.dumps(task_list)
        #print(result)
        conn.set('task_{}'.format(server_uuid), result)

make_instance_tasks()


