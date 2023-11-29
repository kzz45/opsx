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
from django.db.models import Q
from dmonitor.models.task import Task
from dcmdb.models.machine import Machine
from dcmdb.models.mongodb import Mongodb
from dmonitor.models.instance import Instance


def remove_instance_from_monitor():
    all_machines = Machine.objects.filter(Q(external_status="DELETED") | Q(external_status="Stopped")).all()
    for machine in all_machines:
        instance_obj = Instance.objects.filter(endpoint=machine.external_uuid).first()
        if instance_obj:
            print(instance_obj.name)
            instance_obj.labels.clear()
            task_obj = Task.objects.filter(name="基础任务").first()
            remove_instances = task_obj.instances.filter(id=instance_obj.id).first()
            task_obj.instances.remove(remove_instances)
            instance_obj.delete()

    all_mongodb = Mongodb.objects.filter(status=2).all()
    for item in all_mongodb:
        instance_obj = Instance.objects.filter(endpoint=item.external_uuid).first()
        if instance_obj:
            print("delete", "-" * 20, instance_obj.name)
            instance_obj.delete()


remove_instance_from_monitor()
