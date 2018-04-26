# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.


class IPManagement(models.Model):
    """ip地址管理表"""
    ip_address = models.GenericIPAddressField(verbose_name=u"IP地址", unique=True)
    prefix = models.IntegerField(verbose_name=u"子网位数")
    gateway = models.GenericIPAddressField(verbose_name=u"网关", blank=True, null=True)
    person = models.ForeignKey("UserAccess.MyUser", verbose_name=u"使用者", blank=True, null=True)
    allocate_time = models.DateField(verbose_name=u"分配时间", blank=True, null=True)
    end_time = models.DateField(verbose_name=u"回收时间", blank=True, null=True)
    usage = models.TextField(verbose_name=u"用途", blank=True, null=True)
    status = models.ForeignKey("IpStatus", verbose_name=u"状态")
    area = models.ForeignKey("Area", verbose_name=u"分配区域", blank=True, null=True)

    def __unicode__(self):
        return self.ip_address

    class Meta:
        verbose_name = u"IP地址"
        verbose_name_plural = u"IP地址管理表"


class IpStatus(models.Model):
    """ip地址分配状态"""
    status = models.CharField(verbose_name=u"状态", max_length=200, unique=True)
    desc = models.TextField(verbose_name=u"描述", blank=True, null=True)

    def __unicode__(self):
        return self.status

    class Meta:
        verbose_name = u"ip状态"
        verbose_name_plural = u"ip状态管理表"


class Area(models.Model):
    """区域管理表"""
    name = models.CharField(verbose_name=u"名称", max_length=200, unique=True)
    desc = models.TextField(verbose_name=u"描述", blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"区域"
        verbose_name_plural = u"区域管理表"


class AssetManagement(models.Model):
    """部门资产管理表"""
    asset_number = models.IntegerField(verbose_name=u"资产编号", primary_key=True)
    depart = models.ForeignKey("UserAccess.Department", verbose_name=u"所属部门")
    name = models.CharField(verbose_name=u"资产名称", max_length=200)
    property = models.ManyToManyField("AssetProperty", verbose_name=u"资产属性")
    create_time = models.DateField(verbose_name=u"创建日期", auto_now_add=timezone.now)
    desc = models.TextField(verbose_name=u"描述说明", blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"部门资产"
        verbose_name_plural = u"部门资产管理表"


class AssetProperty(models.Model):
    """资产属性映射表"""
    property_name = models.ForeignKey("PropertyName", verbose_name=u"资产名称")
    property_value = models.ForeignKey("PropertyValue", verbose_name=u"资产属性")

    def __unicode__(self):
        return self.property_name.name + "--" + self.property_value.value

    class Meta:
        verbose_name = u"资产属性"
        verbose_name_plural = u"资产属性映射表"


class PropertyName(models.Model):
    """资产名称表"""
    name = models.CharField(verbose_name=u"名称", max_length=200, unique=True)
    desc = models.TextField(verbose_name=u"描述说明", blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"资产名称"
        verbose_name_plural = u"资产名称管理表"


class PropertyValue(models.Model):
    """资产属性表"""
    value = models.CharField(verbose_name=u"属性值", max_length=200, unique=True)
    desc = models.TextField(verbose_name=u"描述说明", blank=True, null=True)

    def __unicode__(self):
        return self.value

    class Meta:
        verbose_name = u"资产属性"
        verbose_name_plural = u"资产属性管理表"


class LifeCycle(models.Model):
    """生命周期"""
    asset = models.OneToOneField("AssetManagement", verbose_name=u"关联资产")
    purchase_time = models.DateField(verbose_name=u"采购时间", blank=True, null=True)
    storage_time = models.DateField(verbose_name=u"入库时间", blank=True, null=True)
    use_time = models.DateField(verbose_name=u"使用时间", blank=True, null=True)
    scrap_time = models.DateField(verbose_name=u"报废时间", blank=True, null=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = u"生命周期"
        verbose_name_plural = u"生命周期管理表"


class AssetRecord(models.Model):
    """资产使用记录"""
    asset = models.ForeignKey("AssetManagement", verbose_name=u"关联资产")
    person = models.ForeignKey("UserAccess.MyUser", verbose_name=u"使用者", blank=True, null=True)
    record_time = models.DateField(verbose_name=u"时间记录", blank=True, null=True)
    use_type = models.ForeignKey("UseType", verbose_name=u"使用类型")
    status = models.BooleanField(verbose_name=u"审核状态", default=False)
    desc = models.TextField(verbose_name=u"使用说明", blank=True, null=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        ordering = ["-id"]
        verbose_name = u"使用记录"
        verbose_name_plural = u"使用记录管理表"


class UseType(models.Model):
    """使用类型"""
    name = models.CharField(verbose_name=u"类型名称", max_length=200, unique=True)
    desc = models.TextField(verbose_name=u"描述说明", blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"使用类型"
        verbose_name_plural = u"使用类型管理表"


