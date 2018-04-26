# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


# Create your models here.

class System(models.Model):
    ip = models.GenericIPAddressField(verbose_name=u"IP地址", primary_key=True)
    mac = models.CharField(verbose_name=u"MAC地址", max_length=100, unique=True)
    nic = models.CharField(verbose_name=u"网口名称", max_length=100)
    profile = models.ForeignKey("Profile", verbose_name=u"配置文件")
    usage = models.CharField(verbose_name=u"机器用途", max_length=255, default=u"未填")
    person_in_charge = models.ForeignKey("UserAccess.MyUser", verbose_name=u"责任人")
    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    desc = models.CharField(verbose_name=u"描述", max_length=200, blank=True, null=True)
    netboot = models.BooleanField(verbose_name=u"启用状态", default=False)
    status = models.BooleanField(verbose_name=u"审核状态", default=False)

    def __unicode__(self):
        return self.ip

    class Meta:
        verbose_name = u"机器实例"
        verbose_name_plural = u"机器实例管理"


class Profile(models.Model):
    name = models.CharField(verbose_name=u"配置名称", max_length=200, unique=True)
    ks = models.ForeignKey("Kickstart", verbose_name=u"ks文件")
    distro = models.ForeignKey("Distro", verbose_name=u"系统镜像")
    owner = models.ForeignKey("UserAccess.MyUser", verbose_name=u"所有者")
    desc = models.CharField(verbose_name=u"描述", max_length=200, blank=True, null=True)
    create_time = models.DateField(verbose_name=u"创建时间", auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"配置文件"
        verbose_name_plural = u"配置文件管理"


class Classify(models.Model):
    name = models.CharField(verbose_name=u"名称", max_length=200, unique=True)
    desc = models.TextField(verbose_name=u"描述", blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"配置文件分类"
        verbose_name_plural = u"配置文件分类管理"


class Kickstart(models.Model):
    name = models.CharField(verbose_name=u"ks名称", max_length=200, unique=True)
    owner = models.ForeignKey("UserAccess.MyUser", verbose_name=u"所属者")
    content = models.TextField(verbose_name=u"KS文件内容")
    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=timezone.now)
    desc = models.TextField(verbose_name=u"描述说明", blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"ks配置文件"
        verbose_name_plural = u"ks配置文件管理"


class Distro(models.Model):
    name = models.CharField(verbose_name=u"系统镜像", max_length=200, unique=True)
    desc = models.TextField(verbose_name=u"描述说明", blank=True, null=True)


class Privilege(models.Model):
    system = models.ForeignKey("System", verbose_name=u"机器实例")
    target_user = models.ForeignKey("UserAccess.MyUser", verbose_name=u"授权用户")
    start_time = models.DateField(verbose_name=u"开始时间")
    end_time = models.DateField(verbose_name=u"结束时间")

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = u"授权"
        verbose_name_plural = u"授权管理"


class LogRecord(models.Model):
    system = models.ForeignKey("System", verbose_name=u"机器实例")
    action = models.TextField(verbose_name=u"操作日志")
    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=timezone.now)
    user = models.ForeignKey("UserAccess.MyUser", verbose_name=u"操作用户")

    def __unicode__(self):
        return self.action

    class Meta:
        verbose_name = u"灌装日志"
        verbose_name_plural = u"灌装日志管理"


