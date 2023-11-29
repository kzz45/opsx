from django.urls import path
from django.contrib import admin
from rest_framework import routers
from django.conf.urls import url, include
from dops.models import UserViewSet, UserGroupViewSet, PermissionViewSet
from dops.views import BasicLogin, BasicLouout

router = routers.DefaultRouter()
router.register("user", UserViewSet)
router.register("perm", PermissionViewSet)
router.register("user_group", UserGroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/cmdb/', include("dcmdb.urls")),
    url(r'^api/monitor/', include("dmonitor.urls")),

    url(r'^api/login/', BasicLogin.as_view()),
    url(r'^api/logout/', BasicLouout.as_view()),
]
