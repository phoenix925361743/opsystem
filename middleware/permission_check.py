#!/usr/bin/env python
# coding:utf-8

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import reverse, HttpResponse


"""检查访问用户权限，通过权限列表进行校验，如果试图访问不允许的url视图，则返回http401"""


class PermissionCheckMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        permission_list = request.session.get("login_user_info").get("login_permission")
        access_url = request.path  # 获取请求访问的url
        if access_url and access_url in permission_list:
            return
        else:
            return HttpResponse(status=403)




