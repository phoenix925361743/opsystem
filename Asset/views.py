# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from UserAccess.models import *
from Asset.models import *
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from DashBoard.models import Notification, Level
import json
import datetime

# Create your views here.


def ip_address(request):
    user = MyUser.objects.get(username=request.session["login_user_info"]["login_user"])
    role = [r.role_name for r in user.role.all()]
    return render(request, "asset/template/ip_address.html", locals())


def ip_address_get(request):
    """ip地址表格渲染"""
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    ip = request.GET.get("ip_address")
    person = request.GET.get("person")
    status = request.GET.get("status")
    area = request.GET.get("area")
    data = {}
    if person:
        data["person"] = MyUser.objects.get(username=person)
    if ip:
        data["ip_address"] = ip
    if status:
        data["status"] = IpStatus.objects.get(status=status)
    if area:
        data["area"] = Area.objects.get(name=area)
    qy = IPManagement.objects.filter(**data)
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
                "ip_address": d.ip_address,
                "prefix": d.prefix,
                "gateway": d.gateway,
                "person": d.person.username if d.person else "",
                "usage": d.usage,
                "allocate_time": d.allocate_time.strftime("%Y-%m-%d") if d.allocate_time else "",
                "end_time": d.end_time.strftime("%Y-%m-%d") if d.end_time else "",
                "status": d.status.status,
                "area": d.area.name if d.area else "",
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


def ip_add_form(request):
    """添加ip地址表单"""
    ip = request.GET.get("ip")
    d = IPManagement.objects.get(ip_address=ip) if ip else []
    return render(request, "asset/template/ip_add_form.html", locals())


def ip_status_get(request):
    """ip状态获取"""
    d = [s.status for s in IpStatus.objects.all()]
    return HttpResponse(json.dumps(d), content_type="application/json")


def area_get(request):
    """分配区域获取"""
    d = [a.name for a in Area.objects.all()]
    return HttpResponse(json.dumps(d), content_type="application/json")


@csrf_exempt
def ip_address_add(request):
    """ip地址添加"""
    if request.method == "POST":
        types = request.POST.get("types")
        person = request.POST.get("person", "")
        allocate_time = request.POST.get("allocate_time", "")
        end_time = request.POST.get("end_time", "")
        usage = request.POST.get("usage", "")
        area = request.POST.get("area", "")
        ip = request.POST.get("ip_address")
        data = {
            "ip_address": ip,
            "prefix": request.POST.get("prefix"),
            "gateway": request.POST.get("gateway"),
            "status": IpStatus.objects.get(status=request.POST.get("status")),
            "person": MyUser.objects.get(username=person) if person else None,
            "allocate_time": datetime.datetime.strptime(allocate_time, "%Y-%m-%d") if allocate_time else None,
            "end_time": datetime.datetime.strptime(end_time, "%Y-%m-%d") if end_time else None,
            "usage": usage,
            "area": Area.objects.get(name=area) if area else None,
        }
        if types == "submit":
            from django.db import IntegrityError
            try:
                IPManagement.objects.create(**data)
            except IntegrityError:
                return HttpResponse("IP地址已存在，请确认!")
        elif types == "update":
            data["person"] = MyUser.objects.get(username=person) if person else ""
            data["area"] = Area.objects.get(name=area) if area else ""
            IPManagement.objects.filter(ip_address=ip).update(**data)
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def ip_delete(request):
    if request.method == "POST":
        ip = request.GET.get("ip")
        IPManagement.objects.filter(ip_address=ip).delete()
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def ip_address_add_batch(request):
    """批量添加IP地址,0为添加成功，1为起始ip段不同，2为开始ip小于结束ip"""
    if request.method == "POST":
        start_ip = request.POST.get("start_ip")
        end_ip = request.POST.get("end_ip")
        prefix = int(request.POST.get("prefix"))
        gateway = request.POST.get("gateway")
        status = IpStatus.objects.get(status="空闲")
        if start_ip[0:start_ip.rfind(".")] != end_ip[0:end_ip.rfind(".")]:
            return HttpResponse(json.dumps([1]))
        else:
            repeat = []
            start = start_ip[0:start_ip.rfind(".")]
            s_ip = int(start_ip.split(".")[-1])
            e_ip = int(end_ip.split(".")[-1])
            from django.db import IntegrityError
            if s_ip > e_ip:
                return HttpResponse(json.dumps(2))
            else:
                for i in range(s_ip, e_ip + 1):
                    ip = start + "." + str(i)
                    try:
                        IPManagement.objects.create(ip_address=ip, prefix=prefix, gateway=gateway, status=status)
                    except IntegrityError:
                        repeat.append(ip)
        if repeat:
            return HttpResponse(json.dumps(repeat))
        else:
            return HttpResponse(json.dumps([0]))
    return HttpResponse("please use post method")


def depart_asset(request):
    """部门资产记录"""
    user = MyUser.objects.get(username=request.session["login_user_info"]["login_user"])
    role = [r.role_name for r in user.role.all()]
    return render(request, "asset/template/depart_asset.html", locals())


def use_type_get(request):
    """获取使用类型"""
    d = [ut.name for ut in UseType.objects.all()]
    return HttpResponse(json.dumps(d), content_type="application/json")


def depart_asset_get(request):
    """部门资产表格渲染"""
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    asset_number = request.GET.get("asset_number")
    asset_name = request.GET.get("asset_name")
    person = request.GET.get("person")
    use_type = request.GET.get("use_type")
    user = request.session["login_user_info"]["login_user"]
    data = {}
    if asset_number:
        data["asset_number"] = int(asset_number)
    if asset_name:
        data["name__icontains"] = asset_name
    if person:
        data["assetrecord__person"] = MyUser.objects.get(username=person)
    qy = AssetManagement.objects.filter(depart=MyUser.objects.get(username=user).depart, **data)
    msg = u"没有数据记录!" if not len(qy) else "ok"
    d_data = {
        "code": 0,
        "msg": msg,
        "count": len(qy),
        "data": [],
    }
    if qy:
        for d in qy[(int(page) - 1) * int(limit):int(page) * int(limit)]:
            r = d.assetrecord_set.all()
            if r:
                latest = r.filter(status=True)
                person = latest[0].person.username if latest[0].person else ""
                if r[0].status:
                    use_type = r[0].use_type.name
                else:
                    use_type = "申请中"
            else:
                person = ""
                use_type = ""
            dd = {
                "asset_number": d.asset_number,
                "name": d.name,
                "person": person,
                "create_time": d.create_time.strftime("%Y-%m-%d"),
                "use_type": use_type,
                "desc": d.desc,
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


def depart_asset_add_form(request):
    """添加部门资产表单"""
    asset_number = request.GET.get("asset_number")
    d = AssetManagement.objects.get(asset_number=int(asset_number)) if asset_number else []
    return render(request, "asset/template/depart_asset_add_form.html", locals())


@csrf_exempt
def depart_asset_add(request):
    """部门资产添加与更新"""
    if request.method == "POST":
        user = request.session["login_user_info"]["login_user"]
        types = request.POST.get("types")
        asset_number = request.POST.get("asset_number")
        data = {
            "asset_number": int(asset_number),
            "depart": MyUser.objects.get(username=user).depart,
            "name": request.POST.get("asset_name"),
            "desc": request.POST.get("desc"),
        }
        if types == "submit":
            try:
                a = AssetManagement.objects.create(**data)
                LifeCycle.objects.create(asset=a)  # 添加默认生命周期信息
                AssetRecord.objects.get_or_create(asset=a, use_type=UseType.objects.get(name="闲置"))  # 新加的资产默认状态为空闲
            except IntegrityError, e:
                return HttpResponse("资产编号 %s 已存在，请确认!" % asset_number)
        elif types == "update":
            AssetManagement.objects.filter(asset_number=int(asset_number)).update(**data)
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def depart_asset_add_batch(request):
    """处理上传的csv数据"""
    if request.method == "POST":
        upload_file = request.FILES["depart_asset_csv"]
        user = request.session["login_user_info"]["login_user"]
        error_data = []
        success_count = 0
        error_count = 0
        for r in upload_file.read().decode("gbk").split("\r\n"):
            if r:
                d = r.split(",")
                try:
                    a = AssetManagement.objects.create(asset_number=int(d[0]), name=d[1],
                                                       depart=MyUser.objects.get(username=user).depart)
                    LifeCycle.objects.create(asset=a)  # 添加默认生命周期信息
                    AssetRecord.objects.get_or_create(asset=a, use_type=UseType.objects.get(name="闲置"),
                                                      record_time=timezone.now(), status=True)  # 新加的资产默认状态为闲置
                    success_count += 1
                except IntegrityError, e:
                    error_data.append(r)
                    error_count += 1
        data = {
            "success_count": success_count,
            "error_count": error_count,
            "error_data": error_data,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return HttpResponse("please use post method")


def depart_asset_detail(request):
    """展示单条资产记录"""
    asset_number = request.GET.get("asset_number")
    user = MyUser.objects.get(username=request.session["login_user_info"]["login_user"])
    if asset_number:
        role = [u.role_name for u in user.role.all()]
        asset = AssetManagement.objects.get(asset_number=int(asset_number))
        propertys = asset.property.all()
        life_cycle = asset.lifecycle
        record = asset.assetrecord_set.filter(status=True)
        return render(request, "asset/template/depart_asset_detail.html", locals())
    return HttpResponse("please give right asset number")


def edit_lifecycle_form(request):
    """编辑资产生命周期信息"""
    asset_number = request.GET.get("asset_number")
    if asset_number:
        asset = AssetManagement.objects.get(asset_number=int(asset_number))
        life_cycle = asset.lifecycle
        return render(request, "asset/template/edit_lifecycle_form.html", locals())
    return HttpResponse("please give the asset number")


@csrf_exempt
def lifecycle_update(request):
    """更新资产生命周期"""
    asset_number = request.POST.get("asset_number")
    purchase_time = request.POST.get("purchase_time", None)
    storage_time = request.POST.get("storage_time", None)
    use_time = request.POST.get("use_time", None)
    scrap_time = request.POST.get("scrap_time", None)
    data = {}
    if purchase_time:
        data['purchase_time'] = purchase_time
    if storage_time:
        data["storage_time"] = storage_time
    if use_time:
        data["use_time"] = use_time
    if scrap_time:
        data["scrap_time"] = scrap_time
    if asset_number:
        asset = AssetManagement.objects.get(asset_number=int(asset_number))
        LifeCycle.objects.filter(asset=asset).update(**data)
        return HttpResponse("ok")
    return HttpResponse("please give right asset number")


@csrf_exempt
def edit_property_form(request):
    """编辑资产属性信息"""
    asset_number = request.GET.get("asset_number")
    if asset_number:
        asset = AssetManagement.objects.get(asset_number=int(asset_number))
        propertys = asset.property.all()
        return render(request, "asset/template/edit_property_form.html", locals())
    return HttpResponse("please give right asset number")


@csrf_exempt
def property_add(request):
    """增加资产属性"""
    if request.method == "POST":
        data = request.POST.get("attribute_data")
        asset_number = request.POST.get("asset_number")
        asset = AssetManagement.objects.get(asset_number=asset_number)
        property_list = []
        for k, v in json.loads(data).items():
            name = PropertyName.objects.get_or_create(name=k)[0]
            value = PropertyValue.objects.get_or_create(value=v)[0]
            p = AssetProperty.objects.get_or_create(property_name=name, property_value=value)[0]
            property_list.append(p)
        asset.property.add(*property_list)
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def delete_property_form(request):
    """删除资产属性"""
    asset_number = request.GET.get("asset_number")
    asset = AssetManagement.objects.get(asset_number=int(asset_number))
    propertys = asset.property.all()
    return render(request, "asset/template/delete_property_form.html", locals())


def property_get(request):
    """渲染属性值表格"""
    asset_number = request.GET.get("asset_number")
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    asset = AssetManagement.objects.get(asset_number=int(asset_number))
    qy = asset.property.all()
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
                "property_name": d.property_name.name,
                "property_value": d.property_value.value,
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


@csrf_exempt
def edit_property(request):
    """编辑资产属性"""
    asset_number = request.GET.get("asset_number")
    if request.method == "GET":
        p_id = request.GET.get("p_id")
        p = AssetProperty.objects.get(id=int(p_id))
        return render(request, "asset/template/edit_property.html", locals())
    if request.method == "POST":
        name = request.POST.get("name")
        value = request.POST.get("value")
        pp_id = request.POST.get("p_id")
        p_name = PropertyName.objects.get_or_create(name=name)[0]
        p_value = PropertyValue.objects.get_or_create(value=value)[0]
        AssetProperty.objects.filter(id=pp_id).update(property_name=p_name, property_value=p_value)
        return HttpResponse("ok")
    return HttpResponse("Oh,I guess you will never see this message!")


@csrf_exempt
def property_delete(request):
    """删除属性"""
    if request.method == "POST":
        batch = request.POST.get("batch")
        if batch:
            id_data = request.POST.get("id_data")
            for i in json.loads(id_data):
                AssetProperty.objects.filter(id=int(i)).delete()
            return HttpResponse("ok")
        else:
            p_id = request.GET.get("p_id")
            AssetProperty.objects.filter(id=int(p_id)).delete()
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def apply_add(request):
    """添加申请记录"""
    if request.method == "POST":
        asset_number = request.POST.get("asset_number")
        user = MyUser.objects.get(username=request.session["login_user_info"]["login_user"])
        desc = request.POST.get("desc")
        use_type = UseType.objects.get(name=request.POST.get("use_type"))
        asset = AssetManagement.objects.get(asset_number=int(asset_number))
        record_time = datetime.datetime.now().strftime("%Y-%m-%d")
        AssetRecord.objects.create(asset=asset, person=user, use_type=use_type, desc=desc, record_time=record_time)
        if use_type.name == u"归还":  # 如果使用状态为归还，则对该资产新建一条状态为闲置的记录
            AssetRecord.objects.create(asset=asset, use_type=UseType.objects.get(name="闲置"), status=True)
        for u in MyUser.objects.filter(role__role_name=u"超级管理员", depart=user.depart):
            data = {
                "user": u,
                "send_user": user.username,
                "message": "%s 于 %s 申请 %s 部门资产 %s--%s, 请审核!" % (user.username, record_time, use_type.name, asset_number, asset.name),
                "level": Level.objects.get(level="INFO"),
            }
            Notification.objects.create(**data)  # 给所有超级管理员发送消息
        return HttpResponse("ok")
    return HttpResponse("please use post method")


def apply_add_form(request):
    """申请资产使用页面渲染"""
    asset_number = request.GET.get("asset_number")
    asset = AssetManagement.objects.get(asset_number=int(asset_number))
    return render(request, "asset/template/apply_add_form.html", locals())


def asset_record_get(request):
    """渲染资产记录审核表格"""
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    qy = AssetRecord.objects.filter(status=False)
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
                "asset_number": d.asset.asset_number,
                "person": d.person.username if d.person else "",
                "record_time": d.record_time.strftime("%Y-%m-%d") if d.record_time else "",
                "use_type": d.use_type.name,
                "desc": d.desc or "",
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


@csrf_exempt
def asset_record_switch(request):
    """审核资产申请记录"""
    if request.method == "POST":
        status = request.POST.get("status")
        s = True if status == "true" else False
        r_id = request.POST.get("r_id")
        AssetRecord.objects.filter(id=int(r_id)).update(status=s)
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def depart_asset_delete(request):
    """删除资产记录"""
    asset_number = request.GET.get("asset_number")
    AssetManagement.objects.filter(asset_number=int(asset_number)).delete()
    return HttpResponse("ok")












