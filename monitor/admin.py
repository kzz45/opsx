from django.contrib import admin

from monitor.models.tmpl import Tmpl
from monitor.models.probe import Probe
from monitor.models.server import Server
from monitor.models.silence import Silence
from monitor.models.instance import Instance
from monitor.models.receiver import Receiver
from monitor.models.alert_rule import AlertRule
from monitor.models.alert_route import AlertRoute
from monitor.models.target_task import TargetTask
from monitor.models.business_task import BusinessTask
from monitor.models.instance_type import InstanceType


class TmplAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "mode"]


class ServerAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "code", "uuid", "ipaddr", "port"]


class InstanceAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "endpoint", "interval", "timeout", "private_ip", "enable", "server", "instance_type"]


class SilenceAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "match", "start", "end", "state", "user", "product"]


class ReceiverAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "channel", "webhook", "product"]


class AlertRuleAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "interval", "expression", "op", "value", "enable", "product"]


class AlertRouteAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "group_wait", "group_interval", "repeat_interval", "match", "enable", "product"]


class TargetTaskAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "match", "args", "product", "server"]


class BusinessTaskAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "url", "interval", "server", "product"]


class InstanceTypeAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "desc"]


admin.site.register(Tmpl, TmplAdmin)
admin.site.register(Probe)
admin.site.register(Server, ServerAdmin)
admin.site.register(Silence, SilenceAdmin)
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Receiver, ReceiverAdmin)
admin.site.register(AlertRule, AlertRuleAdmin)
admin.site.register(AlertRoute, AlertRouteAdmin)
admin.site.register(TargetTask, TargetTaskAdmin)
admin.site.register(InstanceType, InstanceTypeAdmin)
admin.site.register(BusinessTask, BusinessTaskAdmin)
