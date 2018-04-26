#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.shortcuts import HttpResponse, redirect
from UserAccess.function_tools.salt_encrypt import salt_encrypt


def is_login(func):
    def wrapper(request):
        # cookie_id = request.META.get("CSRF_COOKIE", None)
        if request.session.get("login_user_info", None):
            return HttpResponse("<p>你已经登录了,%r</p><a href='/user_access/logout'>注销</a>" % request.session["login_user_info"].get("login_user", "unknown"))
        else:
            return func(request)
    return wrapper


def login_check(func):
    def wrapper(request):
        if request.session.get("login_user_info", None):
            return func(request)
        else:
            return redirect("/user_access/login")
    return wrapper


def encrypt_pass(query_set, raw_pass):
    email = query_set.email
    return salt_encrypt(email, raw_pass)
