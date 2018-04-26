#!/usr/bin/env python
# coding:utf-8

from django.conf.urls import url
from django.views.generic import TemplateView
from Asset import views


urlpatterns = [
    url(r'^ip_address/$', views.ip_address, name="ip_address"),
    url(r'^ip_address/get/$', views.ip_address_get, name="ip_address_get"),
    url(r'^ip/add/form/$', views.ip_add_form, name="ip_add_form"),
    url(r'^ip/status/get/$', views.ip_status_get, name="ip_status_get"),
    url(r'^area/get/$', views.area_get, name="area_get"),
    url(r'^ip_address/add/$', views.ip_address_add, name="ip_address_add"),
    url(r'^ip_address/delete/$', views.ip_delete, name="ip_delete"),
    url(r'^ip_address/add/batch/form/$', TemplateView.as_view(template_name="asset/template/ip_add_batch_form.html"),
        name="ip_add_batch_form"),
    url(r'^ip_address/add/batch/$', views.ip_address_add_batch, name="ip_address_add_batch"),

    url(r'^depart/asset/$', views.depart_asset, name="depart_asset"),
    url(r'^use_type/get/$', views.use_type_get, name="use_type_get"),
    url(r'^depart/asset/get/$', views.depart_asset_get, name="depart_asset_get"),
    url(r'^depart/asset/add/form/$', views.depart_asset_add_form, name="depart_asset_add_form"),
    url(r'^depart/asset/add/$', views.depart_asset_add, name="depart_asset_add"),
    url(r'^depart/asset/add/batch/$', views.depart_asset_add_batch, name="depart_asset_add_batch"),
    url(r'^depart/asset/detail/$', views.depart_asset_detail, name="depart_asset_detail"),
    url(r'^edit/lifecycle/form/$', views.edit_lifecycle_form, name="edit_lifecycle_form"),
    url(r'^lifecycle/update/$', views.lifecycle_update, name="lifecycle_update"),
    url(r'^edit/property/form/$', views.edit_property_form, name="edit_property_form"),
    url(r'^property/add/$', views.property_add, name="property_add"),
    url(r'^property/delete/form/$', views.delete_property_form, name="delete_property_form"),
    url(r'^property/get/$', views.property_get, name="property_get"),
    url(r'^edit/property/$', views.edit_property, name="edit_property"),
    url(r'^property/delete/$', views.property_delete, name="property_delete"),
    url(r'^depart_asset/delete/$', views.depart_asset_delete, name="depart_asset_delete"),

    url(r'^apply/add/$', views.apply_add, name="apply_add"),
    url(r'^apply/add/form/$', views.apply_add_form, name="apply_add_form"),
    url(r'^asset_record/get/$', views.asset_record_get, name="asset_record_get"),
    url(r'^asset_record/switch/$', views.asset_record_switch, name="asset_record_switch"),
]


