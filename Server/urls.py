#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.conf.urls import url
from django.views.generic import TemplateView
from Server import views

urlpatterns = [
    url(r'^index/$', TemplateView.as_view(template_name="server/template/index.html"), name="server_index"),
    url(r'^service/', views.service, name="server_service"),
    url(r'^service_csv/', views.service_csv, name="server_service_csv"),
    url(r'^server/$', views.server, name="server"),
    url(r'^server_info$', views.server_info, name='server_info'),
    url(r'^manufacture$', views.manufacture, name="manufacture"),
    url(r'^model_type$', views.model_type, name="model_type"),
    url(r'^classify$', views.classify, name="classify"),
    url(r'^add_manufacture$', views.add_manufacture, name="addManufacture"),
    url(r'^add_modeltype$', views.add_modeltype, name="addModeltype"),
    url(r'^add_server$', TemplateView.as_view(template_name="server/template/add_server.html"), name="add_server"),
]
