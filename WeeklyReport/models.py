# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class PersonalReport(models.Model):
    """个人周报表"""
    date_period = models.ForeignKey("DatePeriod", verbose_name=u"时间周期")
    job_type = models.ForeignKey("JobType", verbose_name=u"工作类别")
    job_date = models.DateField(verbose_name=u"日期")
    name = models.ForeignKey("UserAccess.MyUser", verbose_name=u"姓名")
    job_code = models.ForeignKey("JobCode", verbose_name=u"工作编号")
    job_time = models.FloatField(verbose_name=u"工时/人力")
    job_content = models.CharField(verbose_name=u"工作内容", max_length=1000)
    job_block = models.CharField(verbose_name=u"工作阻碍", max_length=1000, blank=True, null=True)
    job_status = models.ForeignKey("JobStatus", verbose_name=u"进展状态")
    job_opinion = models.CharField(verbose_name=u"负责人审批意见", max_length=500, blank=True, null=True)
    job_plan = models.CharField(verbose_name=u"明日计划", max_length=1000, blank=True, null=True)
    delete_status = models.BooleanField(verbose_name=u"删除状态", default=False)
    remark = models.CharField(verbose_name=u"备注", max_length=500, blank=True, null=True)
    depart = models.ForeignKey("UserAccess.Department", verbose_name=u"所属部门")
    summary_status = models.ForeignKey("SummaryStatus", verbose_name=u"汇总状态")

    def __unicode__(self):
        return self.name.username

    class Meta:
        verbose_name = u"个人周报"
        verbose_name_plural = u"个人周报管理"
        ordering = ["-job_date"]


class PlanReport(models.Model):
    """下周计划表"""
    date_period = models.ForeignKey("DatePeriod", verbose_name=u"时间周期")
    job_date = models.DateField(verbose_name=u"日期")
    job_type = models.ForeignKey("JobType", verbose_name=u"工作类别")
    name = models.ForeignKey("UserAccess.MyUser", verbose_name=u"姓名")
    job_code = models.ForeignKey("JobCode", verbose_name=u"工作编号")
    job_time = models.FloatField(verbose_name=u"工时/人力")
    job_content = models.CharField(verbose_name=u"工作内容", max_length=1000)
    start_date = models.DateField(verbose_name=u"计划开始日期", blank=True, null=True)
    end_date = models.DateField(verbose_name=u"计划完成日期", blank=True, null=True)
    start_date_r = models.DateField(verbose_name=u"实际开始日期", blank=True, null=True)
    end_date_r = models.DateField(verbose_name=u"实际完成日期", blank=True, null=True)
    job_status = models.ForeignKey("JobStatus", verbose_name=u"进展状态")
    remark = models.CharField(verbose_name=u"备注", max_length=500, blank=True, null=True)
    depart = models.ForeignKey("UserAccess.Department", verbose_name=u"所属部门")

    def __unicode__(self):
        return self.name.username

    class Meta:
        verbose_name_plural = u"下周计划管理"
        verbose_name = u"下周计划"


class SellProject(models.Model):
    """销售支撑与项目执行表"""
    s_id = models.IntegerField(verbose_name=u"ID", primary_key=True)
    job_code = models.ForeignKey("JobCode", verbose_name=u"项目编号")
    project_content = models.CharField(verbose_name=u"项目内容简介", max_length=500)
    job_date = models.DateField(verbose_name=u"日期")
    job_status = models.ForeignKey("JobStatus", verbose_name=u"进展状态")
    next_week_plan = models.CharField(verbose_name=u"下周计划", max_length=500, blank=True, null=True)
    stage_plan = models.CharField(verbose_name=u"总体阶段性计划", max_length=500, blank=True, null=True)
    remark = models.CharField(verbose_name=u"特殊说明", max_length=500, blank=True, null=True)
    depart = models.ForeignKey("UserAccess.Department", verbose_name=u"所属部门")
    date_period = models.ForeignKey("DatePeriod", verbose_name=u"时间周期")
    job_type = models.ForeignKey("JobType", verbose_name=u"工作类型")

    def __unicode__(self):
        return str(self.s_id)

    class Meta:
        verbose_name = u"销售与项目记录"
        verbose_name_plural = u"销售与项目管理"


class ProductDevelopment(models.Model):
    """产品研发管理表"""
    date_period = models.ForeignKey("DatePeriod", verbose_name=u"时间周期")
    product = models.ForeignKey("ProductType", verbose_name=u"产品")
    sub_product = models.ForeignKey("SubProductType", verbose_name=u"子产品")
    job_goal = models.CharField(verbose_name=u"工作目标", max_length=500)
    job_content = models.CharField(verbose_name=u"工作内容", max_length=500)
    summarize = models.CharField(verbose_name=u"工作总结", max_length=5000)
    next_week_plan = models.CharField(verbose_name=u"下周计划", max_length=500, blank=True, null=True)
    stage_plan = models.CharField(verbose_name=u"总体阶段性计划", max_length=500, blank=True, null=True)
    remark = models.CharField(verbose_name=u"特殊说明", max_length=500, blank=True, null=True)
    depart = models.ForeignKey("UserAccess.Department", verbose_name=u"所属部门")

    def __unicode__(self):
        return self.product.type_name

    class Meta:
        verbose_name = u"产品研发记录"
        verbose_name_plural = u"产品研发管理"


class ProductType(models.Model):
    """产品分类"""
    type_name = models.CharField(verbose_name=u"产品分类名称", max_length=200, unique=True)
    desc = models.CharField(verbose_name=u"分类描述", max_length=500, blank=True, null=True)

    def __unicode__(self):
        return self.type_name

    class Meta:
        verbose_name = u"产品分类"
        verbose_name_plural = u"产品分类管理"


class SubProductType(models.Model):
    """产品子分类"""
    type_name = models.ForeignKey("ProductType", verbose_name=u"产品分类名称")
    sub_type_name = models.CharField(verbose_name=u"产品子分类名称", max_length=200, unique=True)
    desc = models.CharField(verbose_name=u"子分类描述", max_length=500, blank=True, null=True)

    def __unicode__(self):
        return self.sub_type_name

    class Meta:
        verbose_name = u"产品子分类"
        verbose_name_plural = u"产品子分类管理"


class StrategicDeployment(models.Model):
    """公司战略部署表"""
    date_period = models.ForeignKey("DatePeriod", verbose_name=u"时间周期")
    job_name = models.CharField(verbose_name=u"工作名称", max_length=500)
    job_goal = models.CharField(verbose_name=u"工作目标", max_length=500)
    job_content = models.CharField(verbose_name=u"工作内容", max_length=500)
    summarize = models.CharField(verbose_name=u"工作总结", max_length=5000)
    next_week_plan = models.CharField(verbose_name=u"下周计划", max_length=500, blank=True, null=True)
    stage_plan = models.CharField(verbose_name=u"阶段性计划", max_length=500, blank=True, null=True)
    remark = models.CharField(verbose_name=u"特殊说明", max_length=500, blank=True, null=True)
    depart = models.ForeignKey("UserAccess.Department", verbose_name=u"所属部门")

    def __unicode__(self):
        return self.job_name

    class Meta:
        verbose_name = u"战略部署"
        verbose_name_plural = u"战略部署管理"


class TeamBuilding(models.Model):
    """团队建设表"""
    date_period = models.ForeignKey("DatePeriod", verbose_name=u"时间周期")
    build_type = models.ForeignKey("BuildType", verbose_name=u"团队建设分类")
    sub_type = models.ForeignKey("SubBuildType", verbose_name=u"团队建设子分类")
    people = models.CharField(verbose_name=u"人员", max_length=300)
    summarize = models.CharField(verbose_name=u"本周总结与得失", max_length=500)
    next_week_plan = models.CharField(verbose_name=u"下周计划", max_length=500, blank=True, null=True)
    stage_plan = models.CharField(verbose_name=u"阶段性计划", max_length=500, blank=True, null=True)
    remark = models.CharField(verbose_name=u"特殊说明", max_length=500, blank=True, null=True)
    depart = models.ForeignKey("UserAccess.Department", verbose_name=u"所属部门")

    def __unicode__(self):
        return self.build_type.type_name

    class Meta:
        verbose_name = u"团队建设"
        verbose_name_plural = u"团队建设管理"


class BuildType(models.Model):
    """团队建设分类"""
    type_name = models.CharField(verbose_name=u"分类名称", max_length=200, unique=True)
    desc = models.CharField(verbose_name=u"分类描述", max_length=500, blank=True, null=True)

    def __unicode__(self):
        return self.type_name

    class Meta:
        verbose_name = u"团队建设分类"
        verbose_name_plural = u"团队建设分类管理"


class SubBuildType(models.Model):
    """团队建设子分类"""
    type_name = models.ForeignKey("BuildType", verbose_name=u"分类名称")
    sub_type_name = models.CharField(verbose_name=u"子分类名称", max_length=200, unique=True)
    desc = models.CharField(verbose_name=u"子分类描述", max_length=500, blank=True, null=True)

    def __unicode__(self):
        return self.sub_type_name

    class Meta:
        verbose_name = u"团队建设子分类"
        verbose_name_plural = u"团队建设子分类管理"


class DatePeriod(models.Model):
    """周报时间周期表"""
    start_date = models.DateField(verbose_name=u"开始日期")
    end_date = models.DateField(verbose_name=u"结束日期")
    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)

    def __unicode__(self):
        return self.start_date.strftime("%Y%m%d") + '-' + self.end_date.strftime("%Y%m%d")

    class Meta:
        ordering = ["-start_date"]
        verbose_name = u"时间周期"
        verbose_name_plural = u"时间周期管理"


class JobType(models.Model):
    """工作类别表"""
    name = models.CharField(verbose_name=u"工作类别", max_length=200, unique=True)
    desc = models.TextField(verbose_name=u"类别描述", blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"工作类别管理"
        verbose_name = u"工作类别"


class JobCode(models.Model):
    """工作编号表"""
    code = models.CharField(verbose_name=u"工作编号", max_length=200, unique=True)
    job_name = models.CharField(verbose_name=u"工作名称", max_length=200, blank=True, null=True)
    old_code = models.CharField(verbose_name=u"旧版编号", max_length=200, blank=True, null=True)
    jf = models.CharField(verbose_name=u"甲方", max_length=200, blank=True, null=True)
    jf_name = models.CharField(verbose_name=u"甲方单位名称", max_length=200, blank=True, null=True)
    person_in_charge = models.CharField(verbose_name=u"我方负责人", max_length=200, default=u"未定")
    desc = models.TextField(verbose_name=u"工作描述", blank=True, null=True)
    status = models.ForeignKey("ProjectStatus", verbose_name=u"项目进度")
    job_type = models.ForeignKey("JobType", verbose_name=u"工作类别")

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name_plural = u"工作编号管理"
        verbose_name = u"工作编号"


class ProjectStatus(models.Model):
    """项目进展状态表"""
    status = models.CharField(verbose_name=u"进展状态", max_length=200, unique=True)
    desc = models.TextField(verbose_name=u"状态描述", blank=True, null=True)

    def __unicode__(self):
        return self.status

    class Meta:
        verbose_name_plural = u"项目进展状态管理"
        verbose_name = u"项目进展状态"


class JobStatus(models.Model):
    """工作进展状态表"""
    status = models.CharField(verbose_name=u"进展状态", max_length=200, unique=True)
    desc = models.TextField(verbose_name=u"状态描述", blank=True, null=True)

    def __unicode__(self):
        return self.status

    class Meta:
        verbose_name_plural = u"进展状态管理"
        verbose_name = u"进展状态"


class SummaryStatus(models.Model):
    """日报汇总状态表"""
    status = models.CharField(verbose_name=u"状态名称", max_length=100, primary_key=True)
    desc = models.TextField(verbose_name=u"详细描述", blank=True, null=True)

    def __unicode__(self):
        return self.status

    class Meta:
        verbose_name_plural = u"汇总状态管理"
        verbose_name = u"汇总状态"
