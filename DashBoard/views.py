# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from DashBoard.models import *
from UserAccess.models import MyUser
from django.views.decorators.csrf import csrf_exempt
import datetime
import json

# Create your views here.


def index(request):
    return render(request, "dashboard/template/index.html")


def page_not_found(request):
    return render(request, "myadmin/media/error/404.html")


def page_error(request):
    return render(request, "myadmin/media/error/500.html")


def not_read_notification_number_get(request):
    user = MyUser.objects.get(username=request.session.get("login_user_info").get("login_user"))
    notification = user.notification_set.all()
    data = {
        "notification_count": notification.count(),
        "not_read_notification_count": notification.filter(read_status=False).count(),
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


def notification_get(request):
    """渲染/重载消息提示的表格数据"""
    user = MyUser.objects.get(username=request.session.get("login_user_info").get("login_user"))
    read_status = request.GET.get("read_status")
    send_user = request.GET.get("send_user")
    level = request.GET.get("level")
    message = request.GET.get("message")
    s = {}
    if read_status:
        s["read_status"] = True if read_status == "True" else False
    if send_user:
        s["send_user"] = send_user
    if level:
        s["level__level"] = level
    if message:
        s["message__icontains"] = message
    if s:
        notification = user.notification_set.filter(**s)
    else:
        notification = user.notification_set.all()
    msg = u"没有数据记录!" if not len(notification) else "ok"
    d_data = {
        "code": 0,
        "msg": msg,
        "count": len(notification),
        "data": [],
    }
    for nf in notification:
        time_difference = datetime.datetime.now() - (nf.create_time + datetime.timedelta(hours=8)).replace(tzinfo=None)
        if time_difference.days:
            t = str(time_difference.days) + u"天"
        elif time_difference.seconds / 3600:
            t = str(time_difference.seconds / 3600) + u"小时"
        elif time_difference.seconds / 60:
            t = str(time_difference.seconds / 60) + u"分钟"
        else:
            t = str(time_difference.seconds) + u"秒"
        m = {
            "id": nf.id,
            "send_user": nf.send_user,
            "time": t,
            "level": nf.level.level,
            "message": nf.message,
            "read_status": "已读" if nf.read_status else "未读",
            "create_time": (nf.create_time + datetime.timedelta(hours=8)).strftime("%Y/%m/%d %H:%M:%S")
        }
        d_data["data"].append(m)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


def level_get(request):
    d = [l.level for l in Level.objects.all()]
    return HttpResponse(json.dumps(d), content_type="application/json")


@csrf_exempt
def change_read_status(request):
    """修改消息阅读状态"""
    if request.method == "POST":
        t = request.POST.get("type")
        n_id = request.POST.get("id")
        if t == "change_true":  # 改变单挑数据记录的阅读状态
            Notification.objects.filter(id=n_id).update(read_status=True)
            return HttpResponse("ok")
        elif t == "mark_true":  # 改变一组标记的数据记录的阅读状态
            id_data = request.POST.get("id_data")
            for i in json.loads(id_data):
                Notification.objects.filter(id=int(i)).update(read_status=True)
            return HttpResponse("ok")
        else:
            return HttpResponse("No type declare")
    return HttpResponse("Please use post method")


@csrf_exempt
def notification_delete(request):
    """删除消息"""
    if request.method == "POST":
        id_data = request.POST.get("id_data")
        for n_id in json.loads(id_data):
            Notification.objects.filter(id=int(n_id)).delete()
        return HttpResponse("ok")
    return HttpResponse("Please use post method")


def system_about(request):
    """系统介绍信息"""
    return render(request, "dashboard/template/about.html", locals())


def memorandum_add_form(request):
    """备忘录表单"""
    return render(request, "dashboard/template/memorandum_add_form.html", locals())


def memorandum_get(request):
    """获取备忘录内容"""
    user = MyUser.objects.get(username=request.session.get("login_user_info").get("login_user"))
    status = request.GET.get("status")
    create_time = request.GET.get("create_time")
    content = request.GET.get("content")
    s = {}
    if status:
        s["status"] = MemorandumStatus.objects.get(name=status)
    if create_time:
        s["create_time"] = create_time
    if content:
        s["content__icontains"] = content
    qy = Memorandum.objects.filter(user=user, **s)
    msg = u"没有数据记录!" if not len(qy) else "ok"
    d_data = {
        "code": 0,
        "msg": msg,
        "count": len(qy),
        "data": [],
    }
    for m in qy:
        dd = {
            "id": m.id,
            "content": m.content,
            "create_time": m.create_time.strftime("%y/%m/%d"),
            "status": m.status.name,
            "remark": m.remark,
        }
        d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


def memorandum_status_get(request):
    """备份状态获取"""
    d = [ms.name for ms in MemorandumStatus.objects.all()]
    return HttpResponse(json.dumps(d), content_type="application/json")


@csrf_exempt
def memorandum_add(request):
    """添加备忘录"""
    if request.method == "POST":
        data = {
            "user": MyUser.objects.get(username=request.session["login_user_info"]["login_user"]),
            "content": request.POST.get("content"),
            "status": MemorandumStatus.objects.get(name="未开始"),
        }
        Memorandum.objects.create(**data)
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def memorandum_edit(request):
    """编辑备忘录"""
    if request.method == "POST":
        qy = Memorandum.objects.filter(id=int(request.POST.get("id")))
        data = {
            "content": request.POST.get("content"),
            "status": MemorandumStatus.objects.get(name=request.POST.get("status")),
            "remark": request.POST.get("remark"),
        }
        qy.update(**data)
        return HttpResponse("ok")
    return HttpResponse("please use post method")


def memorandum_edit_form(request):
    """修改备忘录"""
    d = Memorandum.objects.get(id=request.GET.get("id"))
    return render(request, "dashboard/template/memorandum_edit_form.html", locals())


def version_get(request):
    """获取版本发布记录"""
    data = []
    for version in Version.objects.all():
        html = ""
        content = "<ul>"
        deploy_time = version.deploy_time.strftime("%Y/%m/%d")
        for vi in VersionInfo.objects.filter(version=version):
            content += """<li>%s (%s)</li>""" % (vi.update_info, vi.update_type.name)
        content += "</ul>"
        html += """
            <li class="layui-timeline-item">
                <i class="layui-icon layui-timeline-axis">&#xe63f;</i>
                <div class="layui-timeline-content layui-text">
                    <h3 class="layui-timeline-title"><b>v%s&nbsp;&nbsp;</b><span class="layui-badge-rim">%s</span></h3>
                    %s
                </div>
            </li>
        """ % (version.version, deploy_time, content)
        data.append(html)
    return HttpResponse(json.dumps(data), content_type="application/json")



