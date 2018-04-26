# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from Cobbler.models import *

# Register your models here.


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = (
        'ip', 'mac', 'nic', 'profile', 'usage', 'person_in_charge', 'netboot', 'desc', 'create_time'
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'desc')


@admin.register(Privilege)
class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time')


@admin.register(Kickstart)
class KickstartAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(LogRecord)
class LogRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'system', 'user', 'create_time')

