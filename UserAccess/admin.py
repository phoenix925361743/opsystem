# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


class MyUserInline(admin.TabularInline):
    model = LoginRecord
    max_num = 3


class UserProfileInline(admin.TabularInline):
    model = UserProfile


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = (
        "username", "depart", "email", 'use', "create_time", "modify_time",
    )
    filter_horizontal = ("role",)
    inlines = [
        MyUserInline, UserProfileInline,
    ]
    search_fields = ("username",)
    list_filter = ("use",)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        "permission_name", "permission_value", "create_time",
    )
    search_fields = ("permission_value",)


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = (
        "role_name", "create_time",
    )
    filter_horizontal = ("permission",)


@admin.register(LoginRecord)
class LoginRecordAdmin(admin.ModelAdmin):
    list_display = (
        "login_user", "login_ip", "login_time", "login_exit_time",
    )
    search_fields = ("login_user", "login_ip")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user", "introduce", 'phone', "avatar",
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id", "depart", 'desc',
    )


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = (
        "id", "group_name"
    )
    filter_horizontal = ("group_user", "group_permission")
