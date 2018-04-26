#!/usr/bin/env python
# coding:utf-8

from DashBoard.models import *
from UserAccess.models import *


def notification_create(user, message, level, send_user=u"系统管理员"):
    level = Level.objects.get_or_create(level=level)[0]
    Notification.objects.create(user=user, message=message, level=level, send_user=send_user)
    return

