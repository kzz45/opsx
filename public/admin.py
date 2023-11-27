from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from public.models.factory import Factory
from public.models.product import Product
from public.models.project import Project
from public.models.user_group import UserGroup
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class FactoryAdmin(GuardedModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "desc", "access_id", "access_key"]


class ProductAdmin(GuardedModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "desc", "user_group"]


class ProjectAdmin(GuardedModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "desc", "product"]


class UserGroupAdmin(GuardedModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "admin"]


class PermissionAdmin(GuardedModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "codename", "content_type"]
    list_display_links = ["content_type"]


class ContentTypeAdmin(GuardedModelAdmin):
    ordering = ["id"]
    list_per_page = 15
    list_display = ["id", "name", "app_label", "model"]


admin.site.index_title = "首页"
admin.site.site_header = "运维管理后台"


admin.site.register(Factory, FactoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(UserGroup, UserGroupAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(ContentType, ContentTypeAdmin)
