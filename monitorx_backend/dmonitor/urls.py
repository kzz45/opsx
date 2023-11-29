from django.conf.urls import url, include
from rest_framework import routers

from dmonitor.models.group import GroupViewSet
from dmonitor.models.label import LabelViewSet
from dmonitor.models.label_name import LabelNameViewSet
from dmonitor.models.ticket import TicketViewSet
from dmonitor.models.message import MessageViewSet
from dmonitor.models.silence import SilenceViewSet

from dmonitor.models.alert import AlertViewSet
from dmonitor.models.alert_rule import AlertRuleViewSet
from dmonitor.models.user_group import UserGroupViewSet
from dmonitor.models.alert_route import AlertRouteViewSet
from dmonitor.models.current_alert import CurrentAlertViewSet
from dmonitor.models.alert_rule_type import AlertRuleTypeViewSet
from dmonitor.models.alert_level import AlertLevelViewSet
from dmonitor.models.sls import SLSViewSet

from dmonitor.models.addon import AddOnViewSet
from dmonitor.models.adjust import AdJustViewSet
from dmonitor.models.adcident import AdCidentViewSet
from dmonitor.models.dashboard import DashboardViewSet

from dmonitor.models.task import TaskViewSet
from dmonitor.models.probe import ProbeViewSet
from dmonitor.models.probe_task import ProbeTaskViewSet

from dmonitor.models.instance import InstanceViewSet
from dmonitor.models.instance_type import InstanceTypeViewSet

from dmonitor.models.server import ServerViewSet
from dmonitor.models.server_group import ServerGroupViewSet
from dmonitor.models.callback import CallbackViewSet
# from dmonitor.models.server_group_instance import ServerGroupInstanceViewSet


router = routers.DefaultRouter()
router.register("group", GroupViewSet)
router.register("label", LabelViewSet)
router.register("label_name", LabelNameViewSet)
router.register("ticket", TicketViewSet)
router.register("message", MessageViewSet)
router.register("silence", SilenceViewSet)

router.register("instance", InstanceViewSet)
router.register("instance_type", InstanceTypeViewSet)

router.register("server", ServerViewSet)
router.register("server_group", ServerGroupViewSet)
# router.register("server_group_instance", ServerGroupInstanceViewSet)

router.register("alert", AlertViewSet)
router.register("alert_rule", AlertRuleViewSet)
router.register("user_group", UserGroupViewSet)
router.register("alert_route", AlertRouteViewSet)
router.register("current_alert", CurrentAlertViewSet)
router.register("alert_rule_type", AlertRuleTypeViewSet)
router.register("alert_level", AlertLevelViewSet)

router.register("task", TaskViewSet)
router.register("probe", ProbeViewSet)
router.register("probe_task", ProbeTaskViewSet)

router.register("addon", AddOnViewSet)
router.register("adjust", AdJustViewSet)
router.register("adcident", AdCidentViewSet)
router.register("dashboard", DashboardViewSet)
router.register("sls", SLSViewSet)
router.register("callback", CallbackViewSet)

from dmonitor.views.get_alert_rule import GetAlertRule
from dmonitor.views.get_alert_route import GetAlertRoute
from dmonitor.views.get_tasks import GetTasks
from dmonitor.views.push_labels import PushLabels
from dmonitor.views.alert_wall import AlertWall
from dmonitor.views.get_silence import GetSilence
from dmonitor.views.get_current_alerts import GetCurrentAlert

urlpatterns = [
    url(r"", include(router.urls)),
    url(r'^get_tasks', GetTasks.as_view()),
    url(r'^alert_wall', AlertWall.as_view()),
    url(r'^get_silence', GetSilence.as_view()),
    url(r'^get_alert_rule', GetAlertRule.as_view()),
    url(r'^get_alert_route', GetAlertRoute.as_view()),
    url(r'^get_current_alert', GetCurrentAlert.as_view()),
    url(r'^push_labels', PushLabels.as_view()),
]
