# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'send_user', 'level', 'read_status', 'create_time',
    )
    list_filter = ('level', 'read_status')
    search_fields = ('user',)


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'desc')


@admin.register(WebsiteGuide)
class WebsiteGuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'user',)


@admin.register(Memorandum)
class MemorandumAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'create_time', 'status')


@admin.register(MemorandumStatus)
class MemorandumStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'version', 'desc', 'deploy_time')


@admin.register(VersionInfo)
class VersionInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'version', 'update_type',)


@admin.register(UpdateType)
class VersionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc',)
