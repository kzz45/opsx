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
from dmonitor.models.task import Task
from dmonitor.models.label import Label
from dmonitor.models.instance import Instance
from django_redis import get_redis_connection
conn = get_redis_connection("monitor")


# 实例绑定给任务
def bind_instance_to_task():
    for task in Task.objects.filter(mode=0).all():
        # 任务中配置的过滤规则
        match = json.loads(task.match)
        include_instance_obj = Instance.objects.filter(instance_type=task.instance_type)
        include_labels = []  # 包含的标签
        exclude_labels = []  # 排除的标签
        has_type = False
        for i in match['include']:
            if i['name'] == '_type':
                has_type = True
                continue
            lables = Label.objects.filter(name=i['name']).filter(value=i['value'])
            for label in lables:
                include_labels.append(label)
        if not include_labels and not has_type:
            include_instance_obj = include_instance_obj.filter(product_id=-1)
        for i in match['exclude']:
            for label in Label.objects.filter(name=i['name']).filter(value=i['value']):
                exclude_labels.append(label)
        if include_labels:
            include_instance_obj = include_instance_obj.filter(labels__in=include_labels)
        if exclude_labels:
            include_instance_obj = include_instance_obj.exclude(labels__in=exclude_labels)
        instances = include_instance_obj

        add_instances = instances.exclude(id__in=[i.id for i in task.instances.all()]).all()
        # print("任务中添加实例--->", add_instances)
        task.instances.add(*add_instances)
        remove_instances = task.instances.exclude(id__in=[i.id for i in instances.all()]).all()
        # print("任务中移除实例--->", remove_instances)
        task.instances.remove(*remove_instances)

def instance_count_under_task():
    instance_list = [i.endpoint for i in Instance.objects.filter(instance_type__name="machine").all()]
    print("="*10, instance_list)
    
    for task_obj in Task.objects.filter(instance_type__name="machine").all():
        cache_key = 'task_online_instances_{}'.format(task_obj.id)
        count = task_obj.instances.filter(endpoint__in=instance_list).count()
        print("任务名称--->", task_obj.name, "任务ID--->", task_obj.id, "下实例数量--->", count)
        cache.set(cache_key, count, 3600)
    instance_list = [i.endpoint for i in Instance.objects.filter(instance_type__name="kubernetes").all()]
    for task_obj in Task.objects.filter(instance_type__name="kubernetes").all():
        cache_key = 'task_online_kubernetes_{}'.format(task_obj.id)
        count = task_obj.instances.filter(endpoint__in=instance_list).count()
        print("任务名称--->", task_obj.name, "任务ID--->", task_obj.id, "下实例数量--->", count)
        cache.set(cache_key, count, 3600)



bind_instance_to_task()
instance_count_under_task()
