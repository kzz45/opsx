from rest_framework import routers
from django.conf.urls import url, include

from monitor.models.tmpl import TmplViewSet
from monitor.models.probe import ProbeViewSet
from monitor.models.labels import LabelsViewSet
from monitor.models.server import ServerViewSet
from monitor.models.silence import SilenceViewSet
from monitor.models.callback import CallbackViewSet
from monitor.models.instance import InstanceViewSet
from monitor.models.receiver import ReceiverViewSet
from monitor.models.alert_msg import AlertMsgViewSet
from monitor.models.task_mode import TaskModeViewSet
from monitor.models.dashboard import DashboardViewSet
from monitor.models.probe_task import ProbeTaskViewSet
from monitor.models.alert_rule import AlertRuleViewSet
from monitor.models.alert_route import AlertRouteViewSet
from monitor.models.target_task import TargetTaskViewSet
from monitor.models.current_alert import CurrentAlertViewSet
from monitor.models.business_task import BusinessTaskViewSet
from monitor.models.instance_type import InstanceTypeViewSet
from monitor.models.alert_rule_type import AlertRuleTypeViewSet
from monitor.models.alert_rule_level import AlertRuleLevelViewSet
from monitor.models.alert_rule_child import AlertRuleChildViewSet
from monitor.models.alert_route_child import AlertRouteChildViewSet


router = routers.DefaultRouter()
router.register("tmpl", TmplViewSet)
router.register("probe", ProbeViewSet)
router.register("labels", LabelsViewSet)
router.register("server", ServerViewSet)
router.register("silence", SilenceViewSet)
router.register("callback", CallbackViewSet)
router.register("instance", InstanceViewSet)
router.register("receiver", ReceiverViewSet)
router.register("alert_msg", AlertMsgViewSet)
router.register("task_mode", TaskModeViewSet)
router.register("dashboard", DashboardViewSet)
router.register("probe_task", ProbeTaskViewSet)
router.register("alert_rule", AlertRuleViewSet)
router.register("alert_route", AlertRouteViewSet)
router.register("target_task", TargetTaskViewSet)
router.register("current_alert", CurrentAlertViewSet)
router.register("business_task", BusinessTaskViewSet)
router.register("instance_type", InstanceTypeViewSet)
router.register("alert_rule_type", AlertRuleTypeViewSet)
router.register("alert_rule_level", AlertRuleLevelViewSet)
router.register("alert_rule_child", AlertRuleChildViewSet)
router.register("alert_route_child", AlertRouteChildViewSet)

urlpatterns = [
    url(r"", include(router.urls)),
]
