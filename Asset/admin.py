# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from Asset.models import *

# Register your models here.


@admin.register(IPManagement)
class IPManagementAdmin(admin.ModelAdmin):
    list_display = ("id", "ip_address", "prefix", "gateway", "status")


@admin.register(IpStatus)
class IpStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "status",)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


@admin.register(AssetManagement)
class AssetManagementAdmin(admin.ModelAdmin):
    list_display = ("asset_number", "name", "create_time", "desc")


@admin.register(AssetProperty)
class AssetPropertyAdmin(admin.ModelAdmin):
    list_display = ("id", "property_name", "property_value")


@admin.register(PropertyName)
class PropertyNameAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "desc")


@admin.register(PropertyValue)
class PropertyValueAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "desc")


@admin.register(LifeCycle)
class LifeCycleAdmin(admin.ModelAdmin):
    list_display = ("id", "purchase_time", "storage_time", "use_time", "scrap_time")


@admin.register(AssetRecord)
class AssetRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "asset", "person", "record_time", "use_type", "desc")


@admin.register(UseType)
class UseTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "desc")





