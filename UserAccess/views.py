# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect, reverse
from UserAccess.models import *
from django.views.decorators.csrf import csrf_exempt
from UserAccess.forms import *
from io import BytesIO
from UserAccess.function_tools.auth_code import GenerateAuthCode
from django.utils import timezone
from datetime import datetime, timedelta
import json
import logging


logger = logging.getLogger("default")


@csrf_exempt
def login(request):
    """
    接收用户输入的用户名、密码，通过ajax获取登录返回的状态码，各个状态码的含义如下：
    code=0：账号未启用；
    code=1：用户名（邮箱）或者密码不匹配；
    code=2：登录验证通过。
    :param request: 
    :return: 
    """
    if request.method == "POST":
        message = {}
        form_data = LoginForm(request.POST)
        if form_data.is_valid():
            try:
                login_user_info = form_data.login_authentication  # 获取初步登录的用户信息记录
                if login_user_info["status"]:
                    user = MyUser.objects.get(username=login_user_info["login_user"])
                    if user.use:  # 如果账号未启用，则返回提示
                        login_user_info["cookie_id"] = request.META.get("CSRF_COOKIE")  # 将用户的cookie-id写入登录记录中
                        login_user_info["client_ip"] = request.META.get("REMOTE_ADDR")
                        request.session["login_user_info"] = login_user_info  # 创建记录用户登录状态的session
                        logger.info(
                            "User %s is login from client %r" % (login_user_info["login_user"], request.META.get("REMOTE_ADDR")))
                        message["code"] = "2"
                        LoginRecord.objects.create(login_user=user, login_ip=request.META.get("REMOTE_ADDR"),
                                                   login_time=login_user_info["login_time"])
                    else:
                        message["code"] = "0"
                else:
                    message["code"] = "1"
            except MyUser.DoesNotExist:
                message["code"] = "1"
                del request.session["login_user_info"]
            except KeyError:
                message["code"] = "1"
                del request.session["login_user_info"]
        return HttpResponse(json.dumps(message), content_type="application/json")
    return render(request, "user_access/template/login.html")


def logout(request):
    login_user_info = request.session.get("login_user_info")
    if login_user_info:
        data = {
            "login_time": datetime.strptime(login_user_info["login_time"], "%Y-%m-%d %H:%M:%S"),
            "login_ip": request.META.get("REMOTE_ADDR"),
        }  # 构造登录历史记录表数据
        try:
            user = MyUser.objects.get(username=login_user_info["login_user"])
        except MyUser.DoesNotExist:
            user = MyUser.objects.get(email=data["login_user"])
        lr = LoginRecord.objects.filter(login_user=user, **data)
        if lr:
            lr.update(login_exit_time=timezone.now())  # 更新历史记录数据
        else:
            LoginRecord.objects.create(login_user=user, login_exit_time=timezone.now(), **data)  # 创建历史记录数据
        del request.session["login_user_info"]  # 删除用户登录session
        logger.info("User %s is logout" % login_user_info["login_user"])
        return redirect(reverse("login"))
    return HttpResponse(r"<p>你已经退出该账号，请勿重复注销</p><a href='/UserAccess/login/'>重新登录</a>")


@csrf_exempt
def regist(request):
    if request.method == "POST":
        form_data = RegistForm(request.POST)
        if form_data.is_valid():
            message = {}
            data = form_data.cleaned_data
            role = Roles.objects.get_or_create(role_name=u"用户")  # 默认注册的账号都是普通用户角色
            depart = Department.objects.get_or_create(depart=request.POST.get("depart"))
            from django.db import IntegrityError
            try:
                user = MyUser.objects.create(depart=depart[0], **data)  # 创建账号信息
                user.role = [role[0]]
                UserProfile.objects.get_or_create(user=user)  # 生成用户的配置文件
                message["code"] = "1"
                i = u"用户 %s 从%r注册成功" % (data["username"], request.META.get("REMOTE_ADDR"))
                logger.info(i)
                from DashBoard.function_tools.notification_create import notification_create
                notification_create(user=MyUser.objects.get(username="admin"), message=i, level="INFO")
            except IntegrityError:
                message["code"] = "0"
            return HttpResponse(json.dumps(message), content_type="application/json")
    return render(request, "user_access/template/regist.html")


def create_auth_code(request):
    flow = BytesIO()  # 在内存中开辟空间，临时存放验证码文件
    ca = GenerateAuthCode()
    img, code = ca.create_code()
    request.session["auth_code"] = code
    img.save(flow, "PNG")
    return HttpResponse(flow.getvalue())


def user_info(request):
    login_user = request.session.get("login_user_info")["login_user"]
    query_set = MyUser.objects.get(username=login_user)
    return render(request, "user_access/template/user_profile.html",
                  {"user_info": query_set, "user_profile": query_set.userprofile})


def user_setting(request):
    pass


@csrf_exempt
def change_pass(request):
    if request.method == "POST":
        oldpass = request.POST.get("old_pass")
        newpass = request.POST.get("new_pass")
        login_user_info = request.session.get("login_user_info")
        username = login_user_info.get("login_user")
        query_set = MyUser.objects.filter(username=username)
        message = {}
        if salt_encrypt(login_user_info["login_email"], oldpass) == query_set[0].password:
            query_set.update(password=newpass)
            query_set[0].save()
            message["code"] = "1"  # 成功修改密码后，返回状态为1
            logger.info(
                "User %s change password success" % login_user_info["login_user"])
        else:
            message["code"] = "0"  # 原密码验证失败，返回状态为0
        return HttpResponse(json.dumps(message), content_type="application/json")
    return HttpResponse("post error")


def show_record(request):
    username = request.session["login_user_info"]["login_user"]
    query_set = MyUser.objects.get(username=username)
    login_record = query_set.loginrecord_set.filter()
    data = {}
    html = ""
    if len(login_record) == 0:
        data["code"] = "<font color='blue'>没有更多记录</font>"
    else:
        for record in login_record:
            l_time = (record.login_time + timedelta(hours=8)).strftime("%Y/%m/%d %H:%M:%S")
            e_time = (record.login_exit_time + timedelta(hours=8)).strftime("%Y/%m/%d %H:%M:%S")
            html += r"<font>%r --- %r</font><br/>" % (l_time, e_time)
        data["code"] = html
    return HttpResponse(json.dumps(data), content_type="application/json")


def user_get(request):
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    username = request.GET.get("username")
    qy = MyUser.objects.all()
    if username:
        qy = qy.filter(username__icontains=username)
    msg = u"没有数据记录!" if not len(qy) else "ok"
    d_data = {
        "code": 0,
        "msg": msg,
        "count": len(qy),
        "data": [],
    }
    if qy:
        for d in qy[(int(page) - 1) * int(limit):int(page) * int(limit)]:
            role = ""
            user_group = ""
            role_set = d.role.all()
            group_user_set = d.usergroup_set.all()
            for r in role_set:
                role += r.role_name
                if r.role_name != role_set[len(role_set)-1].role_name:  # 迭代的最后一个元素后面不添加"、"
                    role += r"、"
            for ug in group_user_set:
                user_group += ug.group_name
                if ug.group_name != group_user_set[len(group_user_set)-1].group_name:
                    user_group += r"、"
            dd = {
                "username": d.username,
                "email": d.email,
                "depart": d.depart.depart,
                "role": role,
                "user_group": user_group,
                "phone": d.userprofile.phone,
                "create_time": d.create_time.strftime("%Y-%m-%d"),
                "use": d.use,
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


@csrf_exempt
def user_add_form(request):
    username = request.GET.get("username")
    if username:
        d = MyUser.objects.get(username=username)
    else:
        d = []
    return render(request, "user_access/template/user_add_form.html", locals())


def role_get(request):
    d = [d.role_name for d in Roles.objects.all()]
    return HttpResponse(json.dumps(d), content_type="application/json")


def user_group_get(request):
    d = [d.group_name for d in UserGroup.objects.all()]
    return HttpResponse(json.dumps(d), content_type="application/json")


@csrf_exempt
def use_switch(request):
    if request.method == "POST":
        username = request.POST.get("username")
        status = request.POST.get("status")
        if status == "false":
            MyUser.objects.filter(username=username).update(use=False)
        elif status == "true":
            MyUser.objects.filter(username=username).update(use=True)
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def user_delete(request):
    username = request.GET.get("username")
    MyUser.objects.filter(username=username).delete()
    return HttpResponse("ok")


@csrf_exempt
def user_add(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
            "depart": Department.objects.get(depart=request.POST.get("depart")),
            "password": request.POST.get("password"),
        }
        role = [Roles.objects.get(role_name=r) for r in json.loads(request.POST.get("role"))]
        user_group = [UserGroup.objects.get(group_name=u) for u in json.loads(request.POST.get("user_group"))]
        types = request.POST.get("types")
        if types == "submit":
            user = MyUser.objects.create(**data)
            UserProfile.objects.create(user=user)
            user.role = role
            user.usergroup_set = user_group
        elif types == "update":
            user = MyUser.objects.filter(username=request.POST.get("username"))
            user.update(**data)
            user[0].role = role
            user[0].usergroup_set = user_group
        return HttpResponse("ok")
    return HttpResponse("please use post method")




