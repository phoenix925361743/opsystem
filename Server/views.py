# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, reverse, redirect
from Server.models import *
from function_tools.handleUploadFile import CsvResolve
from function_tools.ssh_tools import SSHResolve
from Server.forms import *
from Server.function_tools.command import shell_command_dict
import json


def service(request):
    if request.method == 'POST':
        form_data = SshInfo(request.POST)
        if form_data.is_valid():
            data = form_data.cleaned_data
            service_data = SSHResolve(data['ssh_ipaddr'], data['ssh_port'], data['ssh_user'], data['ssh_passwd'],
                       command=shell_command_dict).executed_command()
            return render(request, "server/template/service.html", context={"service_data":service_data})
    else:
        form = SshInfo()
        return render(request, "server/template/service.html", context={"form": form})


def service_csv(request):
    if request.method == "POST":
        form_file = SshFileUpload(request.POST, request.FILES)
        if form_file.is_valid():
            try:
                f = form_file.clean_file()
                fdata = CsvResolve(f).csv_read()
                service_data = []
                for connect_info in fdata:
                   service_data.append(SSHResolve(*connect_info,command=shell_command_dict).executed_command())
            except forms.ValidationError:
                service_data = {"error": u"请上传csv格式文件！"}
            return render(request, "server/template/service.html", {"service_data":service_data})
    else:
        form = SshFileUpload()
        return render(request, "server/template/service.html", context={"form":form})


def server(request):
    server_all = Server.objects.all()
    context = {"server_all": server_all}
    return render(request, "server/template/server.html", context=context)


def server_info(request):
    server_id = request.GET.get("server_id")
    if server_id:
        try:
            query_set = Server.objects.get(server_id=int(server_id))
            return render(request, "server/template/server_info.html", context={"qy": query_set})
        except ValueError:
            return HttpResponse("""<p>server_id有错误!</p><a href="/server/server">返回</a>""")
        except Server.DoesNotExist:
            return HttpResponse("""<p>设备不存在，请核实后查询!</p><a href="/server/server">返回</a>""")
    return HttpResponse("""<p>请提供设备ID!</p><a href="/server/server">返回</a>""")


def manufacture(request):
    m_list = [m.name for m in Manufacture.objects.all()]
    return HttpResponse(json.dumps(m_list), content_type="application/json")


def model_type(request):
    manufacture_name = request.GET.get("manufacture")
    query_set = Manufacture.objects.get(name=manufacture_name).modeltype_set.filter()
    t_list = [t.model_type for t in query_set]
    return HttpResponse(json.dumps(t_list), content_type="application/json")


def classify(request):
    c_list = [c.classify_name for c in Classify.objects.all()]
    return HttpResponse(json.dumps(c_list), content_type="application/json")


def add_manufacture(request):
    if request.method == "POST":
        m_name = request.POST.get("name")
        qy = Manufacture.objects.get_or_create(name=m_name)
        return redirect(request.META.get("HTTP_REFERER") or reverse("index"))
    return HttpResponse(u"请使用post方式上传数据")


def add_modeltype(request):
    if request.method == "POST":
        m_list = request.POST.getlist("model_type")
        m_name = request.POST.get("relate_manufacture")
        m_qy = Manufacture.objects.get(name=m_name)
        for mt in m_list:
            ModelType.objects.get_or_create(manufacture=m_qy, model_type=mt)
        return redirect(request.META.get("HTTP_REFERER") or reverse("index"))
    return HttpResponse(u"请使用post方式上传数据")



