#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.shortcuts import HttpResponseRedirect, reverse, HttpResponse, render
from django.utils.deprecation import MiddlewareMixin
from install import initial_setting
from UserAccess.models import MyUser


"""检测用户是否登录的中间件。判断用户的会话消息中是否有登录信息。
如果有，则跳过登录检测；如果没有，则判断访问的url是否在允许非登录状态下访问的列表中，
如果在列表中，则跳过登录检测，如果不在，则将访问重定向至登录页面。
在用户已登录的状态下，同时进行权限校验，校验通过则正常访问，校验失败则返回http403。"""


class LoginCheckMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        request_path = request.path  # 获取请求url
        session = request.session.get("login_user_info")
        if session and session.get("login_user"):
            permission_list = session.get("login_permission")  # 获取用户权限列表
            user = MyUser.objects.get(username=session.get("login_user"))
            if u"超级管理员" in [r.role_name for r in user.role.all()]:  # 超级管理员不设限制
                return
            else:
                if request_path.startswith("/static") or request_path.startswith("/media"):
                    return
                if request_path in permission_list:
                    return
                else:
                    return render(request, "myadmin/media/error/403.html", status=403)
        else:
            allow_path = [
                reverse("login"),  # 登录页面
                reverse("regist"),  # 注册页面
                reverse("auth_code"),  # 验证码
                reverse("depart_get"),  # 部门数据获取
                reverse("listen_get"),  # 灌装监听端口获取
            ]
            if request_path in allow_path:
                return
            else:
                return HttpResponseRedirect(reverse("login"))
