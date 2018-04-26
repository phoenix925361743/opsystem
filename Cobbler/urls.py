#!/usr/bin/env python
# coding:utf-8

from django.conf.urls import url
from django.views.generic import TemplateView
from Cobbler import views


urlpatterns = [
    url(r'^install/$', views.install, name="install"),
    url(r'^system/get/$', views.system_get, name="system_get"),
    url(r'^system/add/form/$', TemplateView.as_view(template_name="cobbler/template/system_add_form.html"),
        name="system_add_form"),
    url(r'^system/add/$', views.system_add, name="system_add"),
    url(r'^system/modify/$', views.system_modify, name="system_modify"),
    url(r'^system/delete/$', views.system_delete, name="system_delete"),
    url(r'^profile/get/$', views.profile_get, name="profile_get"),
    url(r'^install/switch/$', views.install_switch, name="install_switch"),
    url(r'^privilege/manege/$', views.privilege_manage, name="privilege_manage"),
    url(r'^privilege/get/$', views.privilege_get, name="privilege_get"),
    url(r'^privilege/delete/$', views.privilege_delete, name="privilege_delete"),
    url(r'^privilege/add/$', views.privilege_add, name="privilege_add"),
    url(r'^privilege/add/form/$', views.privilege_add_form, name="privilege_add_form"),
    url(r'^profile/add/form/$', views.profile_add_form, name="profile_add_form"),
    url(r'^ks/get/$', views.ks_get, name="ks_get"),
    url(r'^profile/add/$', views.profile_add, name="profile_add"),
    url(r'^distro/get/$', views.distro_get, name="distro_get"),
    url(r'^profile/delete/$', views.profile_delete, name="profile_delete"),
    url(r'^profile/delete/check/$', views.profile_delete_check, name="profile_delete_check"),
    url(r'^system/log/get/$', views.system_log_get, name="system_log_get"),
    url(r'^listen/get/$', views.listen_get, name="listen_get"),
    url(r'^advanced/$', views.advanced, name="cobbler_advanced"),
    url(r'^advanced/system/audit/get/$', views.system_audit_get, name="system_audit_get"),
    url(r'^advanced/system/audit/$', views.system_audit, name="system_audit"),
    url(r'^profile_type/get/$', views.profile_type_get, name="profile_type_get"),
    url(r'^ks/add/form/$', views.ks_add_form, name="ks_add_form"),
    url(r'^ks/add/$', views.ks_add, name="ks_add"),
    url(r'^ks/delete/check/$', views.ks_delete_check, name="ks_delete_check"),
    url(r'^ks/delete/$', views.ks_delete, name="ks_delete"),
]
