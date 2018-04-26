#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django import forms
from UserAccess.models import *
from UserAccess.function_tools.salt_encrypt import salt_encrypt
from UserAccess.function_tools.email_judge import email_judge
from datetime import datetime
from django.shortcuts import reverse, NoReverseMatch


class LoginForm(forms.Form):
    username = forms.CharField(label=u"用户名", max_length=100)
    password = forms.CharField(label=u"密码", max_length=100)

    @property
    def login_authentication(self):
        """
        登录验证。
        """
        data = self.cleaned_data
        login_info = {}
        if email_judge(data["username"]):
            query_set = MyUser.objects.get(email=data["username"])
        else:
            query_set = MyUser.objects.get(username=data["username"])
        post_password = salt_encrypt(query_set.email, data["password"])
        permission = []
        for role in query_set.role.all():  # 迭代用户的角色权限
            for rp in role.permission.all():
                try:
                    permission.append(reverse(rp.permission_value))
                except NoReverseMatch:
                    permission.append(rp.permission_value)  # 如果反向解析失败，则添加原始权限值
        for group in query_set.usergroup_set.all():  # 迭代用户的组权限
            for gp in group.group_permission.all():
                try:
                    permission.append(reverse(gp.permission_value))
                except NoReverseMatch:
                    permission.append(gp.permission_value)
        if query_set.password == post_password:
            login_info = {
                "login_user": query_set.username,
                "login_email": query_set.email,
                "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "login_permission": tuple(set(permission)),
                "avatar": query_set.userprofile.avatar.url,
                "status": True
            }
        else:
            login_info["status"] = False
        return login_info


class RegistForm(forms.Form):
    username = forms.CharField(label=u"用户名", max_length=100)
    password = forms.CharField(label=u"密码", max_length=100)
    email = forms.EmailField(label=u"邮箱地址")
