# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from Cobbler.models import *
from UserAccess.models import MyUser
from install import initial_setting as ini
from Cobbler.function_tools.cobbler_api import CobblerApi
from django.views.decorators.csrf import csrf_exempt
from DashBoard.models import *
from django.core.mail import send_mail
import json
import xmlrpclib
import paramiko
import os


def install(request):
    """渲染自动灌装页面"""
    user = MyUser.objects.get(username=request.session["login_user_info"]["login_user"])
    return render(request, "cobbler/template/install.html", locals())


def system_get(request):
    """获取机器实例"""
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    ip_address = request.GET.get("ip")
    qy = System.objects.all()
    if ip_address:
        qy = qy.filter(ip__icontains=ip_address)
    msg = u"没有数据记录!" if not len(qy) else "ok"
    d_data = {
        "code": 0,
        "msg": msg,
        "count": len(qy),
        "data": [],
    }
    if qy:
        for d in qy[(int(page) - 1) * int(limit):int(page) * int(limit)]:
            privilege_user = [d.person_in_charge.username]
            for p in d.privilege_set.all():
                if int(p.end_time.strftime("%Y%m%d")) < int(datetime.now().strftime("%Y%m%d")):
                    a = p.target_user.username + "(" + p.start_time.strftime("%Y/%m/%d") + "-" + p.end_time.strftime("%Y/%m/%d") + ")"
                    LogRecord.objects.create(system=d, user=MyUser.objects.get(username="admin"), action=u"%s 授权失效" % a)
                    p.delete()  # 如果授权的结束时间小于当前时间，则授权过期，删除
                privilege_user.append(p.target_user.username)  # 添加授权用户的用户名
            dd = {
                "ip": d.ip,
                "mac": d.mac,
                "nic": d.nic,
                "profile": d.profile.name,
                "usage": d.usage,
                "person_in_charge": d.person_in_charge.username,
                "netboot": d.netboot,
                "status": d.status,
                "privilege_user": privilege_user,  # 授权用户列表
                "user": request.session["login_user_info"]["login_user"],  # 当前访问的用户名
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


@csrf_exempt
def system_add(request):
    """添加机器实例"""
    if request.method == "POST":
        ip = request.POST.get("ip")
        mac = request.POST.get("mac")
        nic = request.POST.get("nic")
        profile = request.POST.get("profile")
        usage = request.POST.get("usage")
        types = request.POST.get("types")
        user = MyUser.objects.get(username=request.session["login_user_info"]["login_user"])
        data = {
            "name": ip,
            "hostname": ip,
            "modify_interface": {
                "macaddress-" + nic: mac,
                "ipaddress-" + nic: ip,
                "Gateway-" + nic: "192.168.18.2",
                "subnet-" + nic: "255.255.255.0",
                "static-" + nic: 1,
            },
            "profile": profile,
            "netboot_enabled": False,
        }
        ca = CobblerApi(data)
        if System.objects.filter(ip=ip):
            if types == "update":
                ca.system_modify(ip)
                System.objects.filter(ip=ip).update(ip=ip, mac=mac, nic=nic, usage=usage, profile=Profile.objects.get(name=profile))
                LogRecord.objects.create(system=System.objects.filter(ip=ip)[0], user=user,
                                         action=u"更新机器实例，ip地址为: %s,mac地址为 %s,网口为: %s,用途为: %s,配置文件为: %s" % (ip, mac, nic, usage, profile))
            else:
                return HttpResponse(json.dumps([1]))  # ip已存在
        elif System.objects.filter(mac=mac):
            if types == "update":
                ca.system_modify(ip)
                System.objects.filter(ip=ip).update(ip=ip, mac=mac, nic=nic, usage=usage, person_in_charge=user,
                                                    profile=Profile.objects.get(name=profile))
                LogRecord.objects.create(system=System.objects.filter(ip=ip)[0], user=user,
                                         action=u"更新机器实例，ip地址为: %s,mac地址为 %s,网口为: %s,用途为: %s,配置文件为: %s" % (ip, mac, nic, usage, profile))
            else:
                return HttpResponse(json.dumps([2]))  # mac已存在
        else:
            ca.system_modify()
            System.objects.create(ip=ip, mac=mac, nic=nic, usage=usage, profile=Profile.objects.get(name=profile),
                                  person_in_charge=user)
            Notification.objects.create(user=MyUser.objects.get(username="admin"),
                                        level=Level.objects.get(level="INFO"),
                                        message=u"%s 添加了一个机器实例 %s,请审核!" % (user.username, ip))
            LogRecord.objects.create(system=System.objects.filter(ip=ip)[0], user=user,
                                     action=u"创建机器实例，ip地址为: %s,mac地址为 %s,网口为: %s,用途为: %s,配置文件为: %s" % (ip, mac, nic, usage, profile))
        return HttpResponse(json.dumps([0]))  # 添加成功
    return HttpResponse("please use post method")


def profile_get(request):
    """获取profile"""
    if request.GET.get("table"):
        page = request.GET.get("page")
        limit = request.GET.get("limit")
        name = request.GET.get("name")
        if name:
            qy = Profile.objects.filter(name__icontains=name)
        else:
            qy = Profile.objects.all()
        msg = u"没有数据记录!" if not len(qy) else "ok"
        d_data = {
            "code": 0,
            "msg": msg,
            "count": len(qy),
            "data": [],
        }
        if qy:
            for d in qy[(int(page) - 1) * int(limit):int(page) * int(limit)]:
                dd = {
                    "name": d.name,
                    "ks": d.ks.name,
                    "distro": d.distro.name,
                    "owner": d.owner.username,
                    "create_time": d.create_time.strftime("%Y-%m-%d"),
                    "desc": d.desc,
                }
                d_data["data"].append(dd)
    else:
        classify = request.GET.get("classify")
        if classify is not None:
            d_data = [p.name for p in Profile.objects.filter(classify=ProfileType.objects.get(name=classify))]
        else:
            d_data = [p.name for p in Profile.objects.all()]
    return HttpResponse(json.dumps(d_data), content_type="application/json")


@csrf_exempt
def install_switch(request):
    """启用/禁用灌装开关"""
    if request.method == "POST":
        user = MyUser.objects.get(username=request.session["login_user_info"]["login_user"])
        status = True if request.POST.get("status") == "true" else False
        ip = request.POST.get("ip")
        server = xmlrpclib.Server(ini.cobbler_server)
        token = server.login(ini.cobbler_username, ini.cobbler_password)
        system = server.get_item_handle("system", ip, token)
        server.modify_system(system, "netboot_enabled", status, token)
        server.save_system(system, token)
        server.sync(token)
        System.objects.filter(ip=ip).update(netboot=status)
        if status:
            LogRecord.objects.create(system=System.objects.get(ip=ip), user=user, action=u"开启灌装开关")
        else:
            LogRecord.objects.create(system=System.objects.get(ip=ip), user=user, action=u"禁用灌装开关")
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def listen_get(request):
    """监听客户端发送的数据，并进行相关状态记录,1为安装开始，2为安装结束。"""
    if request.method == "POST":
        user = MyUser.objects.get(username="admin")
        client_data = int(request.POST.get("data"))
        client_ip = request.META.get("REMOTE_ADDR")
        s = System.objects.get(ip=client_ip)
        if client_data == 1:
            server = xmlrpclib.Server(ini.cobbler_server)
            token = server.login(ini.cobbler_username, ini.cobbler_password)
            system = server.get_item_handle("system", client_ip, token)
            server.modify_system(system, "netboot_enabled", False, token)
            server.save_system(system, token)
            server.sync(token)
            System.objects.filter(ip=client_ip).update(netboot=False)
            LogRecord.objects.create(system=s, user=user, action=u"禁用灌装开关,自动灌装开始")
        elif client_data == 2:
            LogRecord.objects.create(system=s, user=user, action=u"自动灌装结束")
            recipient_user = [sys.target_user.email for sys in s.privilege_set.all()]  # 获取机器实例授权用户邮箱
            recipient_user.append(s.person_in_charge.email)  # 获取机器实例所有者邮箱
            send_mail("%s灌装结束" % client_ip, "%s灌装结束，机器正在重启，请稍后确认!" % client_ip, "sre@antiy.cn",
                      recipient_user, fail_silently=False)  # 发送邮件提醒
        elif client_data == 3:
            return HttpResponse(s.nic)
        else:
            pass
        return HttpResponse("ok")
    return HttpResponse("Please use post method")


@csrf_exempt
def system_modify(request):
    """编辑机器信息"""
    ip = request.GET.get("ip")
    d = System.objects.get(ip=ip)
    return render(request, "cobbler/template/system_add_form.html", locals())


@csrf_exempt
def system_delete(request):
    """删除机器信息"""
    ip = request.GET.get("ip")
    System.objects.filter(ip=ip).delete()
    server = xmlrpclib.Server(ini.cobbler_server)
    token = server.login(ini.cobbler_username, ini.cobbler_password)
    server.remove_item("system", ip, token)
    return HttpResponse("ok")


def privilege_manage(request):
    """渲染授权控制页面"""
    ip = request.GET.get("ip")
    d = System.objects.get(ip=ip)
    return render(request, "cobbler/template/privilege_manage_form.html", locals())


def privilege_get(request):
    """渲染授权表格"""
    ip = request.GET.get("ip")
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    qy = System.objects.filter(ip=ip)[0].privilege_set.all()
    msg = u"没有数据记录!" if not len(qy) else "ok"
    d_data = {
        "code": 0,
        "msg": msg,
        "count": len(qy),
        "data": [],
    }
    if qy:
        for d in qy[(int(page) - 1) * int(limit):int(page) * int(limit)]:
            dd = {
                "id": d.id,
                "target_user": d.target_user.username,
                "start_time": d.start_time.strftime("%Y-%m-%d"),
                "end_time": d.end_time.strftime("%Y-%m-%d"),
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


@csrf_exempt
def privilege_delete(request):
    """删除授权"""
    p = Privilege.objects.filter(id=request.GET.get("id"))
    user = MyUser.objects.get(username=request.session["login_user_info"]["login_user"])
    a = p[0].target_user.username + "(" + p[0].start_time.strftime("%Y%m%d") + "--" + p[0].end_time.strftime("%Y%m%d") + ")"
    LogRecord.objects.create(system=p[0].system, user=user, action=u"删除授权：%s" % a)
    p.delete()
    return HttpResponse("ok")


def privilege_add_form(request):
    """渲染system授权表单"""
    ip = request.GET.get("ip")
    return render(request, "cobbler/template/privilege_add_form.html", locals())


@csrf_exempt
def privilege_add(request):
    """添加system授权"""
    if request.method == "POST":
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        target_user = request.POST.get("target_user")
        ip = request.POST.get("ip")
        system = System.objects.get(ip=ip)
        user = MyUser.objects.get(username=target_user)
        Privilege.objects.create(system=system, target_user=user, start_time=start_time, end_time=end_time)
        a = target_user + "(" + start_time.replace("-", "/") + "--" + end_time.replace("-", "/") + ")"
        LogRecord.objects.create(system=system, user=system.person_in_charge, action=u"添加授权:%s" % a)
        return HttpResponse("ok")
    return HttpResponse("please use post method")


def profile_add_form(request):
    """渲染profile表单"""
    user = MyUser.objects.get(username=request.session["login_user_info"]["login_user"])
    return render(request, "cobbler/template/profile_add_form.html", locals())


def profile_delete_check(request):
    """profile删除检查，返回相关联的system列表至前端，给用户进行警醒提示"""
    name = request.GET.get("name")
    d = [s.ip for s in Profile.objects.get(name=name).system_set.all()]
    return HttpResponse(json.dumps(d))


@csrf_exempt
def profile_delete(request):
    """删除profile"""
    if request.method == "POST":
        name = request.GET.get("name")
        print name
        ca = CobblerApi()
        ca.profile_remove(name)
        Profile.objects.filter(name=name).delete()
        return HttpResponse("ok")
    return HttpResponse("please use post method")


def ks_get(request):
    """获取cobbler服务器的ks配置文件"""
    if request.GET.get("table"):
        page = request.GET.get("page")
        limit = request.GET.get("limit")
        name = request.GET.get("name")
        if name:
            qy = Kickstart.objects.filter(name__icontains=name)
        else:
            qy = Kickstart.objects.all()
        msg = u"没有数据记录!" if not len(qy) else "ok"
        d_data = {
            "code": 0,
            "msg": msg,
            "count": len(qy),
            "data": [],
        }
        if qy:
            for d in qy[(int(page) - 1) * int(limit):int(page) * int(limit)]:
                dd = {
                    "name": d.name,
                    "owner": d.owner.username,
                    "create_time": d.create_time.strftime("%Y-%m-%d"),
                    "desc": d.desc,
                }
                d_data["data"].append(dd)
    else:
        d_data = [k.name for k in Kickstart.objects.all()]
    return HttpResponse(json.dumps(d_data), content_type="application/json")


@csrf_exempt
def profile_add(request):
    """添加profile"""
    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "desc": request.POST.get("desc"),
            "ks": Kickstart.objects.get(name=request.POST.get("ks")),
            "distro": Distro.objects.get(name=request.POST.get("distro")),
            "owner": MyUser.objects.get(username=request.session["login_user_info"]["login_user"]),
        }
        profile_data = {
            "name": request.POST.get("name"),
            "kickstart": r"/var/lib/cobbler/kickstarts/" + request.POST.get("ks"),
            "distro": request.POST.get("distro"),
        }
        ca = CobblerApi(profile_data)
        ca.profile_modify()
        Profile.objects.create(**data)
        return HttpResponse("ok")
    return HttpResponse("please use post method")


def distro_get(request):
    """获取distro"""
    ca = CobblerApi()
    d = []
    for distro in ca.get_distro():
        d.append(distro.get("name"))
        Distro.objects.get_or_create(name=distro.get("name"))
    return HttpResponse(json.dumps(d), content_type="application/json")


def profile_type_get(request):
    """配置文件分类获取"""
    d = [pt.name for pt in ProfileType.objects.all()]
    return HttpResponse(json.dumps(d), content_type="application/json")


def system_log_get(request):
    """获取机器实例日志记录"""
    ip = request.GET.get("ip")
    logs = System.objects.get(ip=ip).logrecord_set.all().order_by("-create_time")
    template = """<ul class="layui-timeline">"""
    for log in logs:
        time = (log.create_time + timezone.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        html = """
            <li class="layui-timeline-item">
                <i class="layui-icon layui-timeline-axis"></i>
                <div class="layui-timeline-content layui-text">
                    <div class="layui-timeline-title">%s，%s %s</div>
                </div>
            </li>
        """ % (time, log.user.username, log.action)
        template += html
    template += """</ul>"""
    return HttpResponse(template)


def advanced(request):
    return render(request, "cobbler/template/advanced.html", locals())


def system_audit_get(request):
    """获取未审核的机器实例信息"""
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    qy = System.objects.filter(status=False)
    msg = u"没有数据记录!" if not len(qy) else "ok"
    d_data = {
        "code": 0,
        "msg": msg,
        "count": len(qy),
        "data": [],
    }
    if qy:
        for d in qy[(int(page) - 1) * int(limit):int(page) * int(limit)]:
            dd = {
                "ip": d.ip,
                "mac": d.mac,
                "nic": d.nic,
                "profile": d.profile.name,
                "usage": d.usage,
                "person_in_charge": d.person_in_charge.username,
                "status": d.status,
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


@csrf_exempt
def system_audit(request):
    if request.method == "POST":
        ip = request.POST.get("ip")
        System.objects.filter(ip=ip).update(status=True)
        return HttpResponse("ok")
    return HttpResponse("please use post method")


def ks_add_form(request):
    name = request.GET.get("name")
    if name:
        d = Kickstart.objects.get(name=name)
    else:
        d = []
    return render(request, "cobbler/template/ks_add_form.html", locals())


@csrf_exempt
def ks_add(request):
    """ks文件添加与更新"""
    if request.method == "POST":
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        content = request.POST.get("content")
        t = request.POST.get("types")
        user = MyUser.objects.get(username=request.session["login_user_info"]["login_user"])
        import pexpect
        command = "scp -o StrictHostKeyChecking=no /mnt/%s root@%s:%s/%s" % (
            name, ini.cobbler_server_ip, ini.cobbler_ks_dir, name)
        with open("/mnt/%s" % name, str('w')) as f:
            f.write(content)
        child = pexpect.spawn(command)  #
        child.expect("password")
        child.sendline(ini.cobbler_root_password)
        child.read()
        sync = pexpect.spawn("ssh root@%s 'cobbler sync'" % ini.cobbler_server_ip)
        sync.expect("password")
        sync.sendline(ini.cobbler_root_password)
        sync.read()
        if t == "submit":
            Kickstart.objects.create(owner=user, name=name, desc=desc, content=content)
        elif t == "update":
            Kickstart.objects.filter(name=name).update(desc=desc, content=content)
        os.remove("/mnt/%s" % name)
        return HttpResponse("ok")
    return HttpResponse("please use post method")


def ks_delete_check(request):
    """ks文件删除依赖检测"""
    name = request.GET.get("name")
    ks = Kickstart.objects.get(name=name)
    profile_list = [p.name for p in ks.profile_set.all()]
    system_list = []
    for p in ks.profile_set.all():
        for s in p.system_set.all():
            system_list.append(s.ip)
    return HttpResponse(json.dumps({"profile_list": profile_list, "system_list": system_list}), content_type="application/json")


@csrf_exempt
def ks_delete(request):
    """删除ks文件"""
    if request.method == "POST":
        name = request.GET.get("name")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ini.cobbler_server_ip, 22, str("root"), ini.cobbler_root_password, timeout=5)  # 创建ssh连接，并设置超时时间为5秒
            command = "cd %s && mv ./%s ./ops_delete_bak" % (ini.cobbler_ks_dir, name)
            _, stdout, stderr = ssh.exec_command(str(command))
            if not stderr.read():
                Kickstart.objects.filter(name=name).delete()
            ssh.close()
        except paramiko.AuthenticationException:
            print u"远程主机连接失败，请检查账号密码!"
            return HttpResponse("AuthenticationFail")
        return HttpResponse("ok")
    return HttpResponse("please use post method")



