from rest_framework import routers
from django.conf.urls import url, include
from dcmdb.models.product import ProductViewSet
from dcmdb.models.project import ProjectViewSet
from dcmdb.models.factory import FactoryViewSet
from dcmdb.models.group import GroupViewSet
from dcmdb.models.region import RegionViewSet
from dcmdb.models.zone import ZoneViewSet
from dcmdb.models.vpc import VPCViewSet
from dcmdb.models.subnet import SubnetViewSet
from dcmdb.models.machine_flavor import FlavorViewSet
from dcmdb.models.security import SecurityViewSet
from dcmdb.models.machine import MachineViewSet
from dcmdb.models.mysql import MySQLViewSet
from dcmdb.models.redis import RedisViewSet
from dcmdb.models.mongodb import MongodbViewSet
from dcmdb.models.other import OtherViewSet
from dcmdb.models.domain import DomainViewSet
from dcmdb.models.cert import DomainCertViewSet
from dcmdb.models.domain_record import DomainRecordViewSet
from dcmdb.models.tag import TagViewSet
from dcmdb.models.image import ImageViewSet
from dcmdb.models.slb import SLBViewSet
from dcmdb.models.whitelist import WhiteListViewSet
from dcmdb.models.elastic_ip import ElasticIPViewSet
from dcmdb.models.park import ParkViewSet
from dcmdb.models.building import BuildingViewSet
from dcmdb.models.operator import OperatorViewSet
from dcmdb.models.export_ip import ExportIPViewSet
from dcmdb.models.user_group import UserGroupViewSet
from dcmdb.models.rule import RuleViewSet
from dcmdb.models.role import UserStandardRoleViewSet
from dcmdb.models.user_role_group import UserRoleGroupViewSet
from dcmdb.models.history import HistoryViewSet

router = routers.DefaultRouter()
router.register("product", ProductViewSet)
router.register("project", ProjectViewSet)
router.register("factory", FactoryViewSet)
router.register("group", GroupViewSet)
router.register("vpc", VPCViewSet)
router.register("zone", ZoneViewSet)
router.register("image", ImageViewSet)
router.register("region", RegionViewSet)
router.register("subnet", SubnetViewSet)
router.register("flavor", FlavorViewSet)
router.register("security", SecurityViewSet)
router.register("rule", RuleViewSet)
router.register("machine", MachineViewSet)
router.register("mysql", MySQLViewSet)
router.register("redis", RedisViewSet)
router.register("mongodb", MongodbViewSet)
router.register("other", OtherViewSet)
router.register("cert", DomainCertViewSet)
router.register("domain", DomainViewSet)
router.register("domain_record", DomainRecordViewSet)
router.register("tag", TagViewSet)
router.register("slb", SLBViewSet)
router.register("whitelist", WhiteListViewSet)
router.register("elastic_ip", ElasticIPViewSet)
router.register("park", ParkViewSet)
router.register("building", BuildingViewSet)
router.register("operator", OperatorViewSet)
router.register("export_ip", ExportIPViewSet)
router.register("user_group", UserGroupViewSet)
router.register("role", UserStandardRoleViewSet)
router.register("user_role_group", UserRoleGroupViewSet)
router.register("history", HistoryViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
