from rest_framework import routers
from django.conf.urls import url, include


from public.models.product import ProductViewSet
from public.models.project import ProjectViewSet
from public.models.factory import FactoryViewSet
from public.models.user_group import UserGroupViewSet


router = routers.DefaultRouter()
router.register("product", ProductViewSet)
router.register("project", ProjectViewSet)
router.register("factory", FactoryViewSet)
router.register("user_group", UserGroupViewSet)

urlpatterns = [
    url(r"", include(router.urls)),
]
