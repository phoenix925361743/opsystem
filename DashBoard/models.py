# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.


class Notification(models.Model):
    """消息提示表"""
    user = models.ForeignKey("UserAccess.MyUser", verbose_name=u"所属用户")
    send_user = models.CharField(verbose_name=u"发送用户", max_length=100, default=u"系统管理员")
    message = models.CharField(verbose_name=u"消息", max_length=1000)
    level = models.ForeignKey("Level", verbose_name=u"消息等级")
    read_status = models.BooleanField(verbose_name=u"阅读状态", default=False)
    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=datetime.now)

    def __unicode__(self):
        return self.user.username + "--" + str(self.id)

    class Meta:
        verbose_name = u"消息提示"
        verbose_name_plural = u"消息提示管理表"
        ordering = ["-create_time"]


class Level(models.Model):
    """消息提示等级"""
    level = models.CharField(verbose_name=u"级别", max_length=200, primary_key=True)
    desc = models.CharField(verbose_name=u"级别描述", max_length=1000, blank=True, null=True)

    def __unicode__(self):
        return self.level

    class Meta:
        verbose_name = u"级别"
        verbose_name_plural = u"级别管理表"


class WebsiteGuide(models.Model):
    """网站导航"""
    name = models.CharField(verbose_name=u"网站名称", max_length=100)
    url = models.CharField(verbose_name=u"网址", max_length=100)
    user = models.ForeignKey("UserAccess.MyUser", verbose_name=u"用户")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"网站导航"
        verbose_name_plural = u"网站导航表"


class Memorandum(models.Model):
    """备忘录"""
    user = models.ForeignKey("UserAccess.MyUser", verbose_name=u"用户")
    create_time = models.DateField(verbose_name=u"创建日期", auto_now=timezone.now)
    content = models.TextField(verbose_name=u"备忘内容")
    status = models.ForeignKey("MemorandumStatus", verbose_name=u"状态")
    remark = models.TextField(verbose_name=u"备注说明", blank=True, null=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = u"备忘录"
        verbose_name_plural = u"备忘录管理表"


class MemorandumStatus(models.Model):
    """备忘状态"""
    name = models.CharField(verbose_name=u"名称", max_length=100, unique=True)
    desc = models.TextField(verbose_name=u"描述", blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"备忘状态"
        verbose_name_plural = u"备忘状态管理"


class Version(models.Model):
    """版本记录"""
    version = models.CharField(verbose_name=u"版本号", unique=True, max_length=200)
    deploy_time = models.DateField(verbose_name=u"发布时间")
    desc = models.TextField(verbose_name=u"版本描述", null=True, blank=True)

    def __unicode__(self):
        return self.version

    class Meta:
        ordering = ["-id"]
        verbose_name = u"版本"
        verbose_name_plural = u"版本管理"


class VersionInfo(models.Model):
    """版本更新记录"""
    version = models.ForeignKey("Version", verbose_name=u"版本号")
    update_type = models.ForeignKey("UpdateType", verbose_name=u"更新类型")
    update_info = models.TextField(verbose_name=u"更新记录")

    def __unicode__(self):
        return self.update_info

    class Meta:
        verbose_name = u"更新记录"
        verbose_name_plural = u"更新记录管理"


class UpdateType(models.Model):
    """版本更新类型"""
    name = models.CharField(verbose_name=u"名称", max_length=200, unique=True)
    desc = models.TextField(verbose_name=u"描述", blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"更新类型"
        verbose_name_plural = u"更新类型管理"

