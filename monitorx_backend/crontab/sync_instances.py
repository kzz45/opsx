# -*- coding: utf-8 -*-

import os
os.environ.update({"DJANGO_SETTINGS_MODULE": "dops.settings"})
import django
django.setup()
from django.conf import settings
from django.core.cache import cache

from dmonitor.models.label import Label
from dcmdb.models.machine import Machine
from dmonitor.models.instance import Instance
from django_redis import get_redis_connection
conn = get_redis_connection("monitor")


# 标签差异
def label_difference(info, labels):
    info_keys = set([str(i['name']) + '###' + str(i['value']) for i in info])
    labels_keys = set([str(i.name) + '###' + str(i.value) for i in labels])
    labels_dict = {i.name: i for i in labels}
    need_add = info_keys - labels_keys
    need_del = labels_keys - info_keys
    same = labels_keys & info_keys
    data = {'add': [], 'del': [], 'same': []}
    for i in need_add:
        sp = i.split('###')
        data['add'].append({'name': sp[0], 'value': sp[1]})
    for i in need_del:
        sp = i.split('###')
        data['del'].append({'name': sp[0], 'value': sp[1]})
    for i in same:
        name = i.split('###')[0]
        data['same'].append(labels_dict[name])
    return data


# 实例同步至数据库
def sync_instance_to_db():
    cmdb_info = [{'name': '_type', 'value': 'machine'}]
    all_machines = Machine.objects.all()  # cmdb中所有的机器实例
    # all_machines = Machine.objects.filter(external_uuid='i-uf6afcl6fih9v56i9apu').all()  # cmdb中所有的机器实例
    for machine in all_machines:
        instance_obj = Instance.objects.filter(endpoint=machine.external_uuid).first()  # 是否已经添加到本地监控数据库中
        if not instance_obj:
            instance_obj = Instance(
                name=machine.external_name,
                endpoint=machine.external_uuid,
                private_ip=machine.private_ip,
                public_ip=machine.public_ip,
                product_id=-1,  # 这里的产品在正式上线的时候要真实
                instance_type_id=1  # 默认机器类型
            )
            instance_obj.save()  # 添加到本地监控数据库中
        labels = instance_obj.labels.all()
        difference_info = label_difference(cmdb_info, labels)
        # print("-" * 20, difference_info)
        bind_labeles = difference_info['same']
        if not difference_info['add'] and not difference_info['del']:
            instance_obj.save()

        for label_dict in difference_info['add']:
            if label_dict['name'] in ['_group', '_service', '_project']:
                label = Label.objects.filter(name=label_dict['name']).filter(value=label_dict['value']).filter(product_id=machine.product).first()
                if not label:
                    label = Label(product_id=machine.product, mode=0, name=label_dict['name'], value=label_dict['value'])
                    label.save()
            else:
                label = Label.objects.filter(name=label_dict['name']).filter(value=label_dict['value']).first()
                if not label:
                    label = Label(mode=0, product_id=-1, name=label_dict['name'], value=label_dict['value'])
                    label.save()
            bind_labeles.append(label)

        for label in labels:
            bind_labeles.append(label)
        instance_obj.labels.set(bind_labeles)
        instance_obj.save()


sync_instance_to_db()
