#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.conf.urls import url
from UserAccess import views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^regist$', views.regist, name="regist"),
    url(r'^auth_code$', views.create_auth_code, name="auth_code"),
    url(r'^user_info$', views.user_info, name="user_info"),
    url(r'^user_setting$', views.user_setting, name="user_setting"),
    url(r'^change_pass$', views.change_pass, name="change_pass"),
    url(r'^show_record$', views.show_record, name="show_record"),
    url(r'^change_pass/form/$', TemplateView.as_view(template_name="user_access/template/change_pass_form.html"),
        name="change_pass_form"),
    url(r'^user/manage/$', TemplateView.as_view(template_name="user_access/template/user_manage.html"),
        name="user_manage"),
    url(r'^user/get/$', views.user_get, name="user_get"),
    url(r'^user/add/form/$', views.user_add_form, name="user_add_form"),
    url(r'^user/role/get/$', views.role_get, name="role_get"),
    url(r'^user/user_group/get/$', views.user_group_get, name="user_group_get"),
    url(r'^use/switch/$', views.use_switch, name="use_switch"),
    url(r'^user/delete/$', views.user_delete, name="user_delete"),
    url(r'^user/add/$', views.user_add, name="user_add"),
]
