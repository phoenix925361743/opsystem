#!/usr/bin/env python
# coding:utf-8

from django.core.wsgi import get_wsgi_application
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OPSystem.settings")

application = get_wsgi_application()
