"""opsx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from rest_framework import routers
from django.conf.urls import url, include

from opsx.views.login import Login
from opsx.views.logout import Logout
from opsx.views.register import Register
from opsx.models.user import UserViewSet
from opsx.models.group import GroupViewSet
from opsx.models.perm import PermissionViewSet

router = routers.DefaultRouter()
router.register("user", UserViewSet)
router.register("group", GroupViewSet)
router.register("perm", PermissionViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),

    url(r'^api/login/', Login.as_view()),
    url(r'^api/logout/', Logout.as_view()),
    url(r'^api/register/', Register.as_view()),
    url(r'^api/public/', include("public.urls")),
    url(r'^api/monitor/', include("monitor.urls")),
]
