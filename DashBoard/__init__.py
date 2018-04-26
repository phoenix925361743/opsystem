#!/usr/bin/env python
# coding:utf-8


from django.apps import AppConfig
import os


default_app_config = 'DashBoard.DashBoardConfig'

verbose_name_new = u"仪表板"


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class DashBoardConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = verbose_name_new
