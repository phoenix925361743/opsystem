# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from WeeklyReport.models import *
from django.views.decorators.csrf import csrf_exempt
from UserAccess.models import *
from DashBoard.models import *
from DashBoard.function_tools.notification_create import notification_create
from time import sleep
from django.http import StreamingHttpResponse
import datetime
import json
import xlrd
import xlwt
import os

# Create your views here.


def daily_report(request):
    user = request.session.get("login_user_info").get("login_user")
    personal_report = MyUser.objects.get(username=user).personalreport_set.all()
    return render(request, "weekly_report/template/daily_report.html", context=locals())


def daily_report_data(request):
    """渲染日报记录表格"""
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    job_code = request.GET.get("job_code")
    job_date = request.GET.get("job_date")
    job_content = request.GET.get("job_content")
    date_period = request.GET.get("date_period")
    username = request.session.get("login_user_info").get("login_user")
    qy = MyUser.objects.get(username=username).personalreport_set.all().filter(delete_status=False)
    if job_code:
        qy = qy.filter(job_code__code=job_code)
    if job_date:
        qy = qy.filter(job_date=job_date)
    if job_content:
        qy = qy.filter(job_content__icontains=job_content)
    if date_period:
        dp = DatePeriod.objects.get(start_date=datetime.datetime.strptime(date_period.split("--")[0], "%Y%m%d"))
        qy = qy.filter(date_period=dp)
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
                "r_id": d.id,
                "username": d.name.username,
                "job_type": d.job_type.name,
                "job_date": d.job_date.strftime("%Y-%m-%d"),
                "job_code": d.job_code.code,
                "job_time": d.job_time,
                "job_content": d.job_content,
                "job_block": d.job_block or "",
                "job_plan": d.job_plan or "",
                "job_opinion": d.job_opinion or "",
                "job_status": d.job_status.status,
                "remark": d.remark or "",
                "summary_status": d.summary_status.status,
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


def delete_report_data(request):
    """渲染回收站数据表格"""
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    username = request.session.get("login_user_info").get("login_user")
    qy = MyUser.objects.get(username=username).personalreport_set.all().filter(delete_status=True)
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
                "r_id": d.id,
                "username": d.name.username,
                "job_type": d.job_type.name,
                "job_date": d.job_date.strftime("%Y-%m-%d"),
                "job_code": d.job_code.code,
                "job_time": d.job_time,
                "job_content": d.job_content,
                "job_block": d.job_block or "",
                "job_plan": d.job_plan or "",
                "job_opinion": d.job_opinion or "",
                "job_status": d.job_status.status,
                "summary_status": d.summary_status.status,
                "remark": d.remark or "",
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


def daily_report_add(request):
    """处理提交的日报表单，新增或者更新或者重新提交。"""
    if request.method == "POST":
        post_data = request.POST
        method_type = post_data.get("method_type")  # 获取表单提交的操作类型，如果是add则为新增数据，update则为更新数据
        r_id = post_data.get("r_id")  # 如果是update，则会携带被更新数据的ID
        date_period = post_data["date_period"].split("--")[0]
        user = MyUser.objects.get(username=request.session.get("login_user_info").get("login_user"))
        jt = JobType.objects.get_or_create(name=post_data["job_type"])[0]
        js = JobStatus.objects.get_or_create(status=post_data["job_status"])[0]
        jc = JobCode.objects.get_or_create(code=post_data["job_code"])[0]
        d_period = DatePeriod.objects.get_or_create(
            start_date=datetime.datetime.strptime(date_period, "%Y%m%d").strftime("%Y-%m-%d"))[0]
        ss = SummaryStatus.objects.get(status=u"未审")  # 新增或者更新的日报记录的汇总状态默认为“未审”
        if method_type == "add":  # 执行create
            PersonalReport.objects.get_or_create(date_period=d_period, job_type=jt, job_date=post_data["job_date"],
                                                 name=user, job_code=jc, job_status=js, depart=user.depart,
                                                 job_time=float(post_data["job_time"]), summary_status=ss,
                                                 job_content=post_data["job_content"], remark=post_data["remark"],
                                                 job_plan=post_data["job_plan"], job_block=post_data["job_block"])
        elif method_type == "update":  # 执行update
            qy = PersonalReport.objects.filter(id=int(r_id))
            if qy[0].summary_status.status == u"驳回":
                ss = SummaryStatus.objects.get(status=u"重提")
            try:
                qy.update(date_period=d_period, job_type=jt, job_code=jc, job_date=post_data["job_date"], name=user,
                          job_status=js, job_time=float(post_data["job_time"]), job_content=post_data["job_content"],
                          remark=post_data["remark"], depart=user.depart, job_block=post_data["job_block"],
                          job_plan=post_data["job_plan"], summary_status=ss)
            except ValueError:
                return HttpResponse(u"ID不存在")
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def daily_report_modify(request):
    """渲染编辑日报的表单页面，传递了触发该次编辑的数据内容。PS:这种方式很蠢，但是我没有找到iframe的通讯方式...orz"""
    r_id = request.GET.get("id")
    try:
        d = PersonalReport.objects.get(id=int(r_id))
    except ValueError:
        d = {}
    return render(request, "weekly_report/template/daily_report_add_form.html", locals())


@csrf_exempt
def daily_report_delete(request):
    """接收两个querystring变量。type为操作类型，r_id为日报记录的id。
    其中type的值意义如下：
    0：逻辑删除日报记录（放入回收站）；
    1：物理删除数据（从数据库删除）；
    2：还原数据（从回收站还原到原来位置）。"""
    r_id = request.POST.get("r_id")
    delete_type = request.GET.get("type")
    try:
        if delete_type == "0":
            PersonalReport.objects.filter(id=int(r_id)).update(delete_status=True)
        elif delete_type == "1":
            PersonalReport.objects.filter(id=int(r_id)).delete()
        elif delete_type == "2":
            PersonalReport.objects.filter(id=int(r_id)).update(delete_status=False)
        return HttpResponse("ok")
    except ValueError:
        pass
    return HttpResponse("ID is not a number")


def job_type_get(request):
    d = [jt.name for jt in JobType.objects.all()]
    return HttpResponse(json.dumps(d), content_type="application/json")


def job_code_get(request):
    """项目编号获取"""
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    t = request.GET.get("table")  # 如果传递了table变量，则为渲染表格数据
    job_type = request.GET.get("job_type")
    if t:
        s = request.GET.get("jc_search", "")  # 设置搜索变量
        qy = JobCode.objects.filter(code__icontains=s) or JobCode.objects.filter(old_code__icontains=s)
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
                    "job_name": d.job_name or "",
                    "job_code": d.code,
                    "old_code": d.old_code or "",
                    "jf": d.jf or "",
                    "jf_name": d.jf_name or "",
                    "person_in_charge": d.person_in_charge,
                    "status": d.status.status,
                    "job_type": d.job_type.name,
                }
                d_data["data"].append(dd)
        return HttpResponse(json.dumps(d_data), content_type="application/json")
    if job_type:
        d = [jc.code for jc in JobCode.objects.filter(job_type=JobType.objects.get(name=job_type))]
    else:
        d = [jc.code for jc in JobCode.objects.all()]
    return HttpResponse(json.dumps(d), content_type="application/json")


def depart_get(request):
    """动态获取部门信息，并创建默认部门-测试运维部"""
    Department.objects.get_or_create(depart=u"测试运维部")
    d = [dp.depart for dp in Department.objects.all()]
    return HttpResponse(json.dumps(d), content_type="application/json")


def project_get(request):
    """动态获取项目进展状态，并创建默认值"""
    d = [d.status for d in ProjectStatus.objects.all()]
    return HttpResponse(json.dumps(d), content_type="application/json")


def job_status_get(request):
    """动态获取工作进展状态，并创建默认值"""
    d = [js.status for js in JobStatus.objects.all()]
    return HttpResponse(json.dumps(d), content_type="application/json")


def username_get(request):
    """动态获取当前登录用户所属部门下的所有用户名"""
    curr_username = request.session.get("login_user_info").get("login_user")
    depart = MyUser.objects.get(username=curr_username).depart
    d = [user.username for user in MyUser.objects.filter(depart=depart).exclude(username="admin")]
    return HttpResponse(json.dumps(d), content_type="application/json")


def date_period_get(request):
    """动态获取时间周期信息，并自动创建当前周的时间周期记录"""
    dp = DatePeriod.objects.all()
    now = datetime.datetime.now().date()
    sd = now + datetime.timedelta(days=-(now.weekday()))  # 当前周的周一
    ed = sd + datetime.timedelta(days=6)  # 当前周的周日
    if dp:  # 如果时间周期表不为空，则判断当前日期是否需要创建新的时间周期记录
        if now.strftime("%Y%m%d") >= (dp[0].start_date + datetime.timedelta(days=7)).strftime("%Y%m%d"):
            DatePeriod.objects.create(start_date=sd, end_date=ed)
    else:  # 如果时间周期表为空，则直接创建当前周的时间周期记录
        DatePeriod.objects.create(start_date=sd, end_date=ed)
    d = [dp.start_date.strftime("%Y%m%d") + "--" + dp.end_date.strftime("%Y%m%d") for dp in DatePeriod.objects.all()]
    return HttpResponse(json.dumps(d), content_type="application/json")


def plan_report_get(request):
    """下周计划数据获取"""
    user = MyUser.objects.get(username=request.session["login_user_info"]["login_user"])
    date_period = request.GET.get("date_period")
    if date_period:
        start_date = DatePeriod.objects.get(start_date=datetime.datetime.strptime(date_period.split("--")[0], "%Y%m%d"))
        qy = PlanReport.objects.filter(name=user).filter(date_period=start_date)
    else:
        qy = PlanReport.objects.filter(name=user)
    msg = u"没有数据记录!" if not len(qy) else "ok"
    d_data = {
        "code": 0,
        "msg": msg,
        "count": len(qy),
        "data": [],
    }
    if qy:
        for d in qy:
            dd = {
                "r_id": d.id,
                "username": d.name.username,
                "job_type": d.job_type.name,
                "job_date": d.job_date.strftime("%Y-%m-%d"),
                "job_code": d.job_code.code,
                "job_time": d.job_time,
                "job_content": d.job_content,
                "start_date": d.start_date.strftime("%Y-%m-%d") if d.start_date else "",
                "start_date_r": d.start_date_r.strftime("%Y-%m-%d") if d.start_date_r else "",
                "end_date": d.end_date.strftime("%Y-%m-%d") if d.end_date else "",
                "end_date_r": d.end_date_r.strftime("%Y-%m-%d") if d.end_date_r else "",
                "job_status": d.job_status.status,
                "remark": d.remark or "",
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


def plan_report_add(request):
    """添加下周计划"""
    if request.method == "POST":
        post_data = request.POST
        date_period = post_data["date_period"].split("--")[0]
        user = MyUser.objects.get(username=request.session.get("login_user_info").get("login_user"))
        jt = JobType.objects.get_or_create(name=post_data["job_type"])[0]
        js = JobStatus.objects.get_or_create(status=post_data["job_status"])[0]
        jc = JobCode.objects.get_or_create(code=post_data["job_code"])[0]
        types = post_data["types"]
        r_id = post_data.get("r_id")
        post_date_dict = {}
        if post_data.get("start_date"):
            post_date_dict["start_date"] = post_data["start_date"]
        if post_data.get("start_date_r"):
            post_date_dict["start_date_r"] = post_data["start_date_r"]
        if post_data.get("end_date"):
            post_date_dict["end_date"] = post_data["end_date"]
        if post_data.get("end_date_r"):
            post_date_dict["end_date_r"] = post_data["end_date_r"]
        d_period = DatePeriod.objects.get_or_create(
            start_date=datetime.datetime.strptime(date_period, "%Y%m%d").strftime("%Y-%m-%d"))[0]
        if types == "update":
            PlanReport.objects.filter(id=r_id).update(date_period=d_period, job_type=jt, name=user, job_code=jc,
                                                      job_status=js, depart=user.depart, job_date=post_data["job_date"],
                                                      job_time=float(post_data["job_time"]), remark=post_data["remark"],
                                                      job_content=post_data["job_content"], **post_date_dict)
        elif types == "submit":
            PlanReport.objects.create(date_period=d_period, job_type=jt, name=user, job_code=jc, job_status=js,
                                      job_date=post_data["job_date"], job_time=float(post_data["job_time"]),
                                      job_content=post_data["job_content"], remark=post_data["remark"],
                                      depart=user.depart, **post_date_dict)
        return HttpResponse(json.dumps([0]), content_type="application/json")
    return HttpResponse(json.dumps([1]), content_type="application/json")


@csrf_exempt
def plan_report_delete(request):
    """删除指定下周计划数据"""
    if request.method == "POST":
        r_id = request.POST.get("r_id")
        PlanReport.objects.filter(id=r_id).delete()
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def plan_report_add_form(request):
    """渲染下周计划添加/编辑模板"""
    r_id = request.GET.get("r_id")
    d = PlanReport.objects.get(id=r_id) if r_id else []
    return render(request, "weekly_report/template/plan_report_add_form.html", locals())


def weekly_report_get(request):
    """流加载个人周报汇总"""
    user = MyUser.objects.get(username=request.session.get("login_user_info").get("login_user"))
    data_per_page = 1  # 设置流加载的每页数据数量
    page = request.GET.get("page")
    date_period = DatePeriod.objects.all()[(int(page)-1)*data_per_page:int(page)*data_per_page]
    report_data = {}
    for dp in date_period:
        weekly_report_data = []
        plan_report_data = []
        title = dp.start_date.strftime("%Y%m%d") + " -- " + dp.end_date.strftime("%Y%m%d")
        weekly_report = PersonalReport.objects.filter(name=user).filter(date_period=dp).filter(delete_status=False)
        plan_report = PlanReport.objects.filter(name=user).filter(date_period=dp)
        for wr in weekly_report:
            data1 = {
                "r_id": wr.id,
                "username": wr.name.username,
                "job_type": wr.job_type.name,
                "job_date": wr.job_date.strftime("%Y-%m-%d"),
                "job_code": wr.job_code.code,
                "job_time": wr.job_time,
                "job_content": wr.job_content,
                "job_block": wr.job_block or "",
                "job_plan": wr.job_plan or "",
                "summary_status": wr.summary_status.status,
                "job_status": wr.job_status.status,
                "remark": wr.remark or "",
            }
            weekly_report_data.append(data1)
        for pr in plan_report:
            data2 = {
                "r_id": pr.id,
                "username": pr.name.username,
                "job_type": pr.job_type.name,
                "job_date": pr.job_date.strftime("%Y-%m-%d"),
                "job_code": pr.job_code.code,
                "job_time": pr.job_time,
                "job_content": pr.job_content,
                "start_date": pr.start_date.strftime("%Y-%m-%d") if pr.start_date else "",
                "start_date_r": pr.start_date_r.strftime("%Y-%m-%d") if pr.start_date_r else "",
                "end_date": pr.end_date.strftime("%Y-%m-%d") if pr.end_date else "",
                "end_date_r": pr.end_date_r.strftime("%Y-%m-%d") if pr.end_date_r else "",
                "job_status": pr.job_status.status,
                "remark": pr.remark or "",
            }
            plan_report_data.append(data2)
        report_data[title] = {
            "weekly_report": weekly_report_data,
            "plan_report": plan_report_data,
        }
    page_count = len(DatePeriod.objects.all()) / data_per_page if not len(DatePeriod.objects.all()) % data_per_page else \
        len(DatePeriod.objects.all()) / data_per_page + 1  # 获取数据分页的页码数
    json_data = {
        "page": page,
        "page_count": page_count,
        "report_data": report_data
    }
    return HttpResponse(json.dumps(json_data), content_type="application/json")


def daily_summary_get(request):
    """渲染日报汇总记录表格"""
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    username = request.session.get("login_user_info").get("login_user")
    depart = MyUser.objects.get(username=username).depart.depart
    date_period = request.GET.get("date_period")
    job_code = request.GET.get("job_code")
    user = request.GET.get("username")
    summary_status = request.GET.get("summary_status")
    job_type = request.GET.get("job_type")
    search = {}
    if date_period:
        search["date_period"] = DatePeriod.objects.get(
            start_date=datetime.datetime.strptime(date_period.split("--")[0], "%Y%m%d"))
    if job_code:
        search["job_code"] = JobCode.objects.get(code=job_code)
    if user:
        search["name"] = MyUser.objects.filter(username=user)
    if summary_status:
        search["summary_status"] = SummaryStatus.objects.filter(status=summary_status)
    if job_type:
        search["job_type"] = JobType.objects.get(name=job_type)
    qy = Department.objects.get(depart=depart).personalreport_set.filter(delete_status=False, **search).exclude(
        name=MyUser.objects.get(username="admin"))
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
                "r_id": d.id,
                "username": d.name.username,
                "job_type": d.job_type.name,
                "job_date": d.job_date.strftime("%Y-%m-%d"),
                "job_code": d.job_code.code,
                "job_time": d.job_time,
                "job_content": d.job_content,
                "job_block": d.job_block or "",
                "job_plan": d.job_plan or "",
                "job_opinion": d.job_opinion or "",
                "job_status": d.job_status.status,
                "remark": d.remark or "",
                "summary_status": d.summary_status.status,
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


def plan_summary_get(request):
    """渲染下周计划汇总记录表格"""
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    username = request.session.get("login_user_info").get("login_user")
    depart = MyUser.objects.get(username=username).depart.depart
    date_period = request.GET.get("date_period")
    user = request.GET.get("username")
    search = {}
    if date_period:
        search["date_period"] = DatePeriod.objects.get(
            start_date=datetime.datetime.strptime(date_period.split("--")[0], "%Y%m%d"))
    if user:
        search["name"] = MyUser.objects.filter(username=user)
    qy = Department.objects.get(depart=depart).planreport_set.filter(**search)
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
                "r_id": d.id,
                "username": d.name.username,
                "job_type": d.job_type.name,
                "job_date": d.job_date.strftime("%Y-%m-%d"),
                "job_code": d.job_code.code,
                "job_time": d.job_time,
                "job_content": d.job_content,
                "start_date": d.start_date.strftime("%Y-%m-%d") if d.start_date else "",
                "start_date_r": d.start_date_r.strftime("%Y-%m-%d") if d.start_date_r else "",
                "end_date": d.end_date.strftime("%Y-%m-%d") if d.end_date else "",
                "end_date_r": d.end_date_r.strftime("%Y-%m-%d") if d.end_date_r else "",
                "job_status": d.job_status.status,
                "remark": d.remark,
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


@csrf_exempt
def daily_report_audit(request):
    """日报审核"""
    if request.method == "POST":
        job_opinion = request.POST.get("job_opinion")
        r_id = request.POST.get("r_id")
        t = request.POST.get("types")
        if t == "audit":
            s = SummaryStatus.objects.get_or_create(status=u"通过")[0]
        elif t == "repel":
            s = SummaryStatus.objects.get_or_create(status=u"驳回")[0]
        else:
            s = SummaryStatus.objects.get_or_create(status=u"未审")[0]
        try:
            PersonalReport.objects.filter(id=int(r_id)).update(job_opinion=job_opinion, summary_status=s)
            p = PersonalReport.objects.get(id=int(r_id))
            username = request.session.get("login_user_info").get("login_user")
            u = MyUser.objects.get(username=username)
            if s.status == u"驳回":
                notification_create(message=u"ID为%s的日报被驳回，请检查并重新提交!" % r_id,
                                    level="WARNING", user=p.name, send_user=u)  # 驳回日报发送消息
                SellProject.objects.filter(s_id=int(r_id)).delete()  # 删除进入汇总表的日报记录
            elif s.status == u"通过":
                if p.job_type.name == u"项目类" or p.job_type.name == u"科研项目":
                    SellProject.objects.create(s_id=int(r_id), job_code=p.job_code, project_content=p.job_content,
                                               job_date=p.job_date, job_status=p.job_status, remark=p.remark or "",
                                               date_period=p.date_period, depart=p.depart, job_type=p.job_type)  # 汇总项目类日报
            else:
                pass
        except ValueError:
            return HttpResponse(u"ID不存在")
    return HttpResponse(u"请使用post方式上传数据")


@csrf_exempt
def daily_report_audit_batch(request):
    """批量审核日报"""
    if request.method == "POST":
        id_data = request.POST.get("id_data")
        s = SummaryStatus.objects.get(status=u"通过")
        for i in json.loads(id_data):
            p = PersonalReport.objects.get(id=int(i))
            PersonalReport.objects.filter(id=int(i)).update(job_opinion=u"批量审核通过", summary_status=s)
            if p.job_type.name == u"项目类" or p.job_type.name == u"科研项目":
                SellProject.objects.update_or_create(s_id=int(i), job_code=p.job_code, project_content=p.job_content,
                                                     job_date=p.job_date, job_status=p.job_status, depart=p.depart,
                                                     date_period=p.date_period, job_type=p.job_type,
                                                     remark=p.remark or "")  # 汇总项目类日报
        return HttpResponse("ok")
    return HttpResponse("Please use post method")


def summary_status_get(request):
    ss = [s.status for s in SummaryStatus.objects.all()]
    return HttpResponse(json.dumps(ss), content_type="application/json")


def sell_project_get(request):
    dp = DatePeriod.objects.all()[0]
    depart = MyUser.objects.get(username=request.session["login_user_info"]["login_user"]).depart
    t = request.GET.get("types")
    jt = JobType.objects.get_or_create(name=u"科研项目")[0] if t == "study" else JobType.objects.get_or_create(name=u"项目类")[0]
    dr = SellProject.objects.filter(job_type=jt, date_period=dp, depart=depart)  # 获取当前周的销售与项目类日报
    json_data = []
    for sp in dr:
        data = {
            "job_code": sp.job_code.code,
            "project_content": sp.project_content,
            "job_date": sp.job_date.strftime("%Y-%m-%d"),
            "job_status": sp.job_status.status,
            "next_week_plan": sp.next_week_plan or "",
            "stage_plan": sp.stage_plan or "",
            "remark": sp.remark or "",
        }
        json_data.append(data)
    return HttpResponse(json.dumps(json_data), content_type="application/json")


def this_week_get(request):
    dp = DatePeriod.objects.all()[0]
    return HttpResponse(json.dumps([dp.start_date.strftime("%Y%m%d") + "--" + dp.end_date.strftime("%Y%m%d")]),
                        content_type="application/json")


def product_type_get(request):
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    t = request.GET.get("table")  # 如果传递了table变量，则为渲染表格数据
    if t:
        s = request.GET.get("pt_search", "")  # 设置搜索变量
        qy = ProductType.objects.filter(type_name__icontains=s)
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
                    "type_name": d.type_name,
                    "desc": d.desc or "",
                }
                d_data["data"].append(dd)
        return HttpResponse(json.dumps(d_data), content_type="application/json")
    else:
        p = [p.type_name for p in ProductType.objects.all()]
    return HttpResponse(json.dumps(p), content_type="application/json")


def sub_product_get(request):
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    t = request.GET.get("table")  # 如果传递了table变量，则为渲染表格数据
    if t:
        sleep(0.1)  # 延迟0.1s加载表格，防止删除产品分类后，同步获取产品子分类出现异常（假装和product_type_get这个函数是异步的......）
        s = request.GET.get("spt_search", "")  # 设置搜索变量
        if s:
            qy = SubProductType.objects.filter(type_name=s)
        else:
            qy = SubProductType.objects.all()
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
                    "type_name": d.type_name.type_name,
                    "sub_type_name": d.sub_type_name,
                    "desc": d.desc or "",
                }
                d_data["data"].append(dd)
        return HttpResponse(json.dumps(d_data), content_type="application/json")
    else:
        p = ProductType.objects.get(type_name=request.GET.get("product"))
        sp = [p.sub_type_name for p in SubProductType.objects.filter(type_name=p)]
    return HttpResponse(json.dumps(sp), content_type="application/json")


def product_development_add(request):
    """添加产品研发类周报记录"""
    if request.method == "POST":
        start_date = request.POST.get("date_period").split("--")[0]
        data = {
            "date_period": DatePeriod.objects.get(start_date=datetime.datetime.strptime(start_date, "%Y%m%d")),
            "product": ProductType.objects.get(type_name=request.POST.get("product")),
            "sub_product": SubProductType.objects.get(sub_type_name=request.POST.get("sub_product")),
            "job_goal": request.POST.get("job_goal"),
            "job_content": request.POST.get("job_content"),
            "summarize": request.POST.get("summarize"),
            "next_week_plan": request.POST.get("next_week_plan") or "",
            "stage_plan": request.POST.get("stage_plan") or "",
            "remark": request.POST.get("remark") or "",
            "depart": MyUser.objects.get(username=request.session["login_user_info"]["login_user"]).depart,
        }  # 构造表单数据字典
        ProductDevelopment.objects.create(**data)
        return HttpResponse("ok")
    return HttpResponse("Please use post method")


def product_development_get(request):
    """获取产品研发类周报数据"""
    dp = DatePeriod.objects.all()[0]
    depart = MyUser.objects.get(username=request.session["login_user_info"]["login_user"]).depart
    pd = ProductDevelopment.objects.filter(date_period=dp, depart=depart)
    json_data = []
    if pd:
        for d in pd:
            data = {
                "id": d.id,
                "product": d.product.type_name,
                "sub_product": d.sub_product.sub_type_name,
                "job_goal": d.job_goal,
                "job_content": d.job_content,
                "summarize": d.summarize or "",
                "next_week_plan": d.next_week_plan or "",
                "stage_plan": d.stage_plan or "",
                "remark": d.remark or "",
            }
            json_data.append(data)
    return HttpResponse(json.dumps(json_data), content_type="application/json")


def product_development_table_get(request):
    """渲染产品开发类数据表格"""
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    date_period = request.GET.get("date_period")
    depart = MyUser.objects.get(username=request.session["login_user_info"]["login_user"]).depart
    search = {}
    if date_period:
        search["date_period"] = DatePeriod.objects.get(start_date=datetime.datetime.strptime(date_period.split("--")[0], "%Y%m%d"))
    qy = ProductDevelopment.objects.filter(depart=depart, **search)
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
                "product": d.product.type_name,
                "sub_product": d.sub_product.sub_type_name,
                "job_goal": d.job_goal,
                "job_content": d.job_content,
                "summarize": d.summarize or "",
                "next_week_plan": d.next_week_plan or "",
                "stage_plan": d.stage_plan or "",
                "remark": d.remark or "",
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


@csrf_exempt
def product_development_delete(request):
    if request.method == "POST":
        id_data = request.POST.get("id_data")
        for r_id in json.loads(id_data):
            try:
                ProductDevelopment.objects.filter(id=int(r_id)).delete()
            except ProductDevelopment.DoesNotExist:
                pass
        return HttpResponse("ok")
    return HttpResponse("please use post method")


def strategic_deployment_get(request):
    """获取公司战略部署周报数据"""
    dp = DatePeriod.objects.all()[0]
    depart = MyUser.objects.get(username=request.session["login_user_info"]["login_user"]).depart
    pd = StrategicDeployment.objects.filter(date_period=dp, depart=depart)
    json_data = []
    if pd:
        for d in pd:
            data = {
                "id": d.id,
                "job_name": d.job_name,
                "job_goal": d.job_goal,
                "job_content": d.job_content,
                "summarize": d.summarize or "",
                "next_week_plan": d.next_week_plan or "",
                "stage_plan": d.stage_plan or "",
                "remark": d.remark or "",
            }
            json_data.append(data)
    return HttpResponse(json.dumps(json_data), content_type="application/json")


@csrf_exempt
def strategic_deployment_delete(request):
    if request.method == "POST":
        id_data = request.POST.get("id_data")
        for r_id in json.loads(id_data):
            try:
                StrategicDeployment.objects.filter(id=int(r_id)).delete()
            except StrategicDeployment.DoesNotExist:
                pass
        return HttpResponse("ok")
    return HttpResponse("please use post method")


def strategic_deployment_add(request):
    """添加公司战略部署周报记录"""
    if request.method == "POST":
        start_date = request.POST.get("date_period").split("--")[0]
        depart = MyUser.objects.get(username=request.session["login_user_info"]["login_user"]).depart
        data = {
            "date_period": DatePeriod.objects.get(start_date=datetime.datetime.strptime(start_date, "%Y%m%d")),
            "job_name": request.POST.get("job_name"),
            "job_goal": request.POST.get("job_goal"),
            "job_content": request.POST.get("job_content"),
            "summarize": request.POST.get("summarize"),
            "next_week_plan": request.POST.get("next_week_plan") or "",
            "stage_plan": request.POST.get("stage_plan") or "",
            "remark": request.POST.get("remark") or "",
            "depart": depart,
        }  # 构造表单数据字典
        StrategicDeployment.objects.create(**data)
        return HttpResponse("ok")
    return HttpResponse("Please use post method")


def strategic_deployment_table_get(request):
    """渲染公司战略部署数据表格"""
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    date_period = request.GET.get("date_period")
    depart = MyUser.objects.get(username=request.session["login_user_info"]["login_user"]).depart
    search = {}
    if date_period:
        search["date_period"] = DatePeriod.objects.get(
            start_date=datetime.datetime.strptime(date_period.split("--")[0], "%Y%m%d"))
    qy = StrategicDeployment.objects.filter(depart=depart, **search)
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
                "job_name": d.job_name,
                "job_goal": d.job_goal,
                "job_content": d.job_content,
                "summarize": d.summarize or "",
                "next_week_plan": d.next_week_plan or "",
                "stage_plan": d.stage_plan or "",
                "remark": d.remark or "",
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


def team_building_get(request):
    """获取团队建设周报数据"""
    dp = DatePeriod.objects.all()[0]
    depart = MyUser.objects.get(username=request.session["login_user_info"]["login_user"]).depart
    tb = TeamBuilding.objects.filter(date_period=dp, depart=depart)
    json_data = []
    if tb:
        for d in tb:
            data = {
                "id": d.id,
                "build_type": d.build_type.type_name,
                "sub_type": d.sub_type.sub_type_name,
                "people": d.people,
                "summarize": d.summarize or "",
                "next_week_plan": d.next_week_plan or "",
                "stage_plan": d.stage_plan or "",
                "remark": d.remark or "",
            }
            json_data.append(data)
    return HttpResponse(json.dumps(json_data), content_type="application/json")


def team_building_add(request):
    """添加团队建设周报记录"""
    if request.method == "POST":
        start_date = request.POST.get("date_period").split("--")[0]
        depart = MyUser.objects.get(username=request.session["login_user_info"]["login_user"]).depart
        data = {
            "date_period": DatePeriod.objects.get(start_date=datetime.datetime.strptime(start_date, "%Y%m%d")),
            "build_type": BuildType.objects.get(type_name=request.POST.get("build_type")),
            "sub_type": SubBuildType.objects.get(sub_type_name=request.POST.get("sub_type")),
            "people": request.POST.get("people"),
            "summarize": request.POST.get("summarize"),
            "next_week_plan": request.POST.get("next_week_plan") or "",
            "stage_plan": request.POST.get("stage_plan") or "",
            "remark": request.POST.get("remark") or "",
            "depart": depart,
        }  # 构造表单数据字典
        TeamBuilding.objects.create(**data)
        return HttpResponse("ok")
    return HttpResponse("Please use post method")


def build_type_get(request):
    bt = [d.type_name for d in BuildType.objects.all()]
    return HttpResponse(json.dumps(bt), content_type="application/json")


def sub_build_type_get(request):
    bt = request.GET.get("build_type")
    sbt = [d.sub_type_name for d in SubBuildType.objects.filter(type_name=BuildType.objects.get(type_name=bt))]
    return HttpResponse(json.dumps(sbt), content_type="application/json")


def team_building_table_get(request):
    """渲染团队建设数据表格"""
    page = request.GET.get("page")
    limit = request.GET.get("limit")
    date_period = request.GET.get("date_period")
    depart = MyUser.objects.get(username=request.session["login_user_info"]["login_user"]).depart
    search = {}
    if date_period:
        search["date_period"] = DatePeriod.objects.get(
            start_date=datetime.datetime.strptime(date_period.split("--")[0], "%Y%m%d"))
    qy = TeamBuilding.objects.filter(depart=depart, **search)
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
                "build_type": d.build_type.type_name,
                "sub_type": d.sub_type.sub_type_name,
                "people": d.people,
                "summarize": d.summarize,
                "next_week_plan": d.next_week_plan or "",
                "stage_plan": d.stage_plan or "",
                "remark": d.remark or "",
            }
            d_data["data"].append(dd)
    return HttpResponse(json.dumps(d_data), content_type="application/json")


@csrf_exempt
def team_building_delete(request):
    if request.method == "POST":
        id_data = request.POST.get("id_data")
        for r_id in json.loads(id_data):
            try:
                TeamBuilding.objects.filter(id=int(r_id)).delete()
            except TeamBuilding.DoesNotExist:
                pass
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def job_code_add(request):
    """创建或者更新工作编号数据"""
    if request.method == "POST":
        data = {
            "job_name": request.POST.get("job_name") or "",
            "code": request.POST.get("job_code"),
            "old_code": request.POST.get("old_code") or "",
            "jf": request.POST.get("jf") or "",
            "jf_name": request.POST.get("jf_name") or "",
            "person_in_charge": request.POST.get("person_in_charge") or u"未定",
            "status": ProjectStatus.objects.get(status=request.POST.get("status")),
            "job_type": JobType.objects.get(name=request.POST.get("job_type"))
        }
        if request.POST.get("j_id"):
            JobCode.objects.filter(id=int(request.POST.get("j_id"))).update(**data)  # post的数据中有编号ID则更新，否则创建
        else:
            JobCode.objects.create(**data)
        return HttpResponse("ok")
    return HttpResponse("please use post method")


def job_code_add_form(request):
    """生成项目编号表单"""
    j_id = request.GET.get("id")
    try:
        jc_record = JobCode.objects.get(id=int(j_id))
    except:
        jc_record = None
    return render(request, "weekly_report/template/job_code_add_form.html", locals())


@csrf_exempt
def job_code_delete(request):
    """删除项目编号"""
    if request.method == "POST":
        j_id = request.POST.get("j_id")
        JobCode.objects.filter(id=int(j_id)).delete()
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def product_type_add(request):
    """添加产品分类"""
    if request.method == "POST":
        type_name = request.POST.get("type_name")
        desc = request.POST.get("desc", "")
        ProductType.objects.get_or_create(type_name=type_name, desc=desc)
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def sub_product_add(request):
    """添加产品子分类"""
    if request.method == "POST":
        type_name = request.POST.get("type_name")
        sub_type_name = request.POST.get("sub_type_name")
        desc = request.POST.get("desc", "")
        SubProductType.objects.get_or_create(type_name=ProductType.objects.get(type_name=type_name),
                                             desc=desc, sub_type_name=sub_type_name)
        return HttpResponse("ok")
    return HttpResponse("please use post method")


def product_type_add_form(request):
    """生成产品分类表单"""
    j_id = request.GET.get("id")
    try:
        pt_record = ProductType.objects.get(id=int(j_id))
    except:
        pt_record = None
    return render(request, "weekly_report/template/product_type_add_form.html", locals())


def sub_product_add_form(request):
    """生成产品子分类表单"""
    j_id = request.GET.get("id")
    try:
        spt_record = SubProductType.objects.get(id=int(j_id))
    except:
        spt_record = None
    return render(request, "weekly_report/template/sub_product_add_form.html", locals())


@csrf_exempt
def product_type_delete(request):
    """删除产品分类"""
    if request.method == "POST":
        j_id = request.POST.get("j_id")
        ProductType.objects.filter(id=int(j_id)).delete()
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def sub_product_delete(request):
    """删除产品子分类"""
    if request.method == "POST":
        j_id = request.POST.get("j_id")
        SubProductType.objects.filter(id=int(j_id)).delete()
        return HttpResponse("ok")
    return HttpResponse("please use post method")


@csrf_exempt
def job_code_upload(request):
    """处理上传的工作编号文件并读取数据创建数据记录"""
    if request.method == 'POST':
        upload_file = request.FILES["job_code_excel"]
        f_sheet = xlrd.open_workbook(file_contents=upload_file.read()).sheets()[0]  # 获取excel的第一个sheet
        error_count = 0  # 创建失败的数目
        success_count = 0  # 创建成功的数目
        error_row = []  # 创建失败的数据所在的excel中的行数
        for i in range(f_sheet.nrows):
            r = f_sheet.row_values(i)
            if len(r) >= 8:
                jt = r[7]
                status = r[6]
            elif r[2].lower().startswith("c"):
                jt = JobType.objects.get_or_create(name=u"产品类")[0]
                status = ProjectStatus.objects.get_or_create(status=u"未定")[0]
            elif r[2].lower().startswith("w"):
                jt = JobType.objects.get_or_create(name=u"部门事务类")[0]
                status = ProjectStatus.objects.get_or_create(status=u"内部")[0]
            else:
                jt = JobType.objects.get_or_create(name=u"项目类")[0]
                status = ProjectStatus.objects.get_or_create(status=u"未定")[0]
            data = {
                "job_name": r[0] or "",
                "old_code": r[1] or "",
                "code": r[2],
                "jf": r[3] or "",
                "jf_name": r[4] or "",
                "person_in_charge": r[5] or u"未确定",
                "status": status,
                "job_type": jt,
            }
            try:
                jc = JobCode.objects.get_or_create(**data)
                if jc[1]:
                    success_count += 1
            except:
                error_row.append(i+1)
                error_count += 1  # 统计创建失败的数目
        try:
            e = JobCode.objects.filter(job_name=u"工作名称", old_code=u"工作编号", code=u"新编号")  # 删除行标题创建的数据
            e.delete()
        except JobCode.DoesNotExist:
            pass
        r_data = {
            "status": "ok",
            "error_count": error_count,
            "success_count": success_count,
            "error_row": error_row,
        }
        return HttpResponse(json.dumps(r_data), content_type="application/json")
    return HttpResponse("Please use post method")


@csrf_exempt
def export_weekly_report(request):
    """导出当前周的周报，生成excel文件并提供下载与文件保存"""
    if request.method == "POST":
        date_period = request.POST.get("date_period2")
        dp = DatePeriod.objects.get(start_date=datetime.datetime.strptime(date_period.split("-")[0], "%Y%m%d"))  # 获取传递的时间周期对象
        from WeeklyReport.function_tools import WriteToExcel
        wbook = WriteToExcel.write_to_excel(request, dp)
        # 保存excel文件并返回至前端
        dp_str = dp.start_date.strftime("%Y%m%d") + "_" + dp.end_date.strftime("%Y%m%d")  # 格式化日期字符串
        response = HttpResponse(content_type='application/vnd.ms-excel')  # 设置mime类型
        response['Content-Disposition'] = 'attachment; filename=' + dp_str + '.xls'  # 设置下载响应协议Content-Disposition
        save_path = "static/weekly_report/weekly_report_history/(京)测试运维部周报-%s.xls" % dp_str
        if os.path.exists(save_path):
            os.remove(save_path)
        wbook.save(save_path)  # 保存历史文件
        wbook.save(response)  # 返回至前端提供下载
        return response
    return HttpResponse("please use post method")


@csrf_exempt
def export_daily_report(request):
    """导出指定周的个人周报,生成excel文件并提供下载"""
    if request.method == "POST":
        date_period = request.POST.get("date_period1")
        dp = DatePeriod.objects.get(start_date=datetime.datetime.strptime(date_period.split("-")[0], "%Y%m%d"))
        from WeeklyReport.function_tools import WriteToExcel
        wbook = WriteToExcel.export_daily_report(request, dp)
        response = HttpResponse(content_type='application/vnd.ms-excel')  # 设置mime类型
        response['Content-Disposition'] = 'attachment; filename=' + date_period + '.xls'  # 设置下载响应协议Content-Disposition
        wbook.save(response)  # 返回至前端提供下载
        return response
    return HttpResponse("please use post method")





