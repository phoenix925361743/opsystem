# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.


class AttributeMapAdminInline(admin.TabularInline):
    model = AttributeMap
    can_delete = True


class LifeCycleAdminInline(admin.TabularInline):
    model = LifeCycle
    can_delete = True


class RemoteInfoAdminInline(admin.TabularInline):
    model = RemoteInfo
    can_delete = True


class ModelTypeAdminInline(admin.TabularInline):
    model = ModelType
    can_delete = True


@admin.register(Manufacture)
class ManufactureAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )
    inlines = (ModelTypeAdminInline, )


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = (
        "server_id", "ipaddr", "classify_id", "serial_number", "manufacture", "status", "person", "create_time",
    )
    inlines = (AttributeMapAdminInline, LifeCycleAdminInline, RemoteInfoAdminInline)


@admin.register(LifeCycle)
class LifeCycleAdmin(admin.ModelAdmin):
    list_display = (
        "server_id", "purchase_time", "storage_time", "scrap_time",
    )


@admin.register(Classify)
class ClassifyAdmin(admin.ModelAdmin):
    list_display = (
        "id", "classify_name",
    )


@admin.register(AttributeMap)
class AttributeMapAdmin(admin.ModelAdmin):
    list_display = (
        "server_id", "map_desc", "attribute_id", "attribute_value_id",
    )


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    pass


@admin.register(CabinetClassify)
class CabinetClassifyAdmin(admin.ModelAdmin):
    pass


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = (
        "id", "attribute_name", "attribute_desc",
    )


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = (
        "id", "attribute_value", "attribute_value_desc",
    )


@admin.register(ModelType)
class ModelTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass

@admin.register(ConnectType)
class ConnectTypeAdmin(admin.ModelAdmin):
    pass