#!/usr/bin/env python
# coding:utf-8

from django.conf.urls import url
from django.views.generic import TemplateView
from DashBoard import views


urlpatterns = [
    url(r'^unread_notification_number/get/$', views.not_read_notification_number_get,
        name="not_read_notification_number_get"),
    url(r'^notification/get/$', views.notification_get, name="notification_get"),
    url(r'^notification/form/$', TemplateView.as_view(template_name="dashboard/template/notification_form.html"),
        name="notification_form"),
    url(r'^level_get/$', views.level_get, name="level_get"),
    url(r'^read_status/change/$', views.change_read_status, name="change_read_status"),
    url(r'^notification/delete/$', views.notification_delete, name="notification_delete"),
    url(r'^system/about/$', views.system_about, name="system_about"),
    url(r'^memorandum/add/form/$', views.memorandum_add_form, name="memorandum_add_form"),
    url(r'^memorandum/get/$', views.memorandum_get, name="memorandum_get"),
    url(r'^memorandum/status/get/$', views.memorandum_status_get, name='memorandum_status_get'),
    url(r'^memorandum/add/$', views.memorandum_add, name="memorandum_add"),
    url(r'^memorandum/edit/form/$', views.memorandum_edit_form, name="memorandum_edit_form"),
    url(r'^memorandum/edit/$', views.memorandum_edit, name="memorandum_edit"),
    url(r'^version/get/$', views.version_get, name="version_get"),
]
