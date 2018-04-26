#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from UserAccess.models import *
from django.http import HttpResponse


def permission_require(request, permission_value):
    """
    视图访问权限控制装饰器，接收两个参数作为权限控制的判断依据。
    :param request: 当前视图的request，主要用于获取当前发起request的用户信息获取;
    :param permission_value: 当前视图访问所需要的权限属性;
    :return: None
    """
    current_user = request.session["session_info"]["login_user"]  # 获取当前登录用户信息
    current_user_permission = [
        p.permission_value for p in MyUser.objects.get(username=current_user).role.permission.all()
    ]
    if permission_value in current_user_permission:
        def _permission_require(func):
            def wrapper():
                return func
            return wrapper
    else:
        def _permission_require(func):
            return HttpResponse(u"你没有权限访问")
    return _permission_require
