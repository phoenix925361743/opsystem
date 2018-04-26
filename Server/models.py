# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.


class Cabinet(models.Model):
    asset_number = models.ForeignKey("Asset.AssetNumber", verbose_name=u"资产编号")
    cabinet_classify = models.ForeignKey("CabinetClassify", verbose_name=u"机柜分类")
    cabinet_name = models.CharField(verbose_name=u"机柜名称", max_length=100)

    def __unicode__(self):
        return self.cabinet_name

    class Meta:
        verbose_name = u"机柜"
        verbose_name_plural = u"机柜管理表"


class CabinetClassify(models.Model):
    name = models.CharField(verbose_name=u"分类名称", max_length=100, unique=True)
    description = models.CharField(verbose_name=u"分类描述", max_length=500, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"机柜分类"
        verbose_name_plural = u"机柜分类管理表"


class Server(models.Model):
    server_id = models.AutoField(verbose_name=u"设备ID", primary_key=True)
    asset_number = models.ForeignKey("Asset.AssetNumber", verbose_name=u"资产编号")
    cabinet = models.ForeignKey("Cabinet", verbose_name=u"机柜", blank=True, null=True)
    manufacture = models.ForeignKey("Manufacture", verbose_name=u"设备厂商")
    model_type = models.ForeignKey("ModelType", verbose_name=u"设备型号")
    classify = models.ForeignKey("Classify", verbose_name=u"分类ID", related_name="classify")
    STATUS = (
        (None, u"选择状态"),
        ("1", u"在用"),
        ("2", u"闲置"),
        ("3", u"损坏"),
        ("4", u"报废"),
        ("5", u"借出"),
        ("6", u"借入"),
        ("7", u"其他"),
    )
    ipaddr = models.ForeignKey("Asset.IPManagement", verbose_name=u"管理IP", null=True, blank=True)
    status = models.CharField(verbose_name=u"设备状态", choices=STATUS, max_length=10)
    person = models.ForeignKey("Person", verbose_name=u"责任人")
    serial_number = models.CharField(verbose_name=u"序列号", max_length=50, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name=u"记录创建时间", auto_now_add=timezone.now)
    modify_time = models.DateTimeField(verbose_name=u"记录修改时间", auto_now=timezone.now)
    delete_status = models.BooleanField(verbose_name=u"删除状态", default=False)

    def __unicode__(self):
        if self.ipaddr:
            return self.ipaddr.ip_address
        return self.serial_number or str(self.server_id)

    class Meta:
        verbose_name_plural = u"设备管理表"
        verbose_name = u"设备"


class Manufacture(models.Model):
    name = models.CharField(verbose_name=u"厂商", max_length=50, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"设备厂商"
        verbose_name_plural = u"设备厂商管理表"


class ModelType(models.Model):
    manufacture = models.ForeignKey("Manufacture", verbose_name=u"设备厂商")
    model_type = models.CharField(verbose_name=u"设备型号", max_length=50, unique=True)

    def __unicode__(self):
        return self.model_type

    class Meta:
        verbose_name_plural = u"设备型号管理表"
        verbose_name = u"设备型号"


class LifeCycle(models.Model):
    server_id = models.OneToOneField("Server", verbose_name=u"设备")
    purchase_time = models.DateField(verbose_name=u"采购时间", null=True, blank=True)
    storage_time = models.DateField(verbose_name=u"入库时间", null=True, blank=True)
    scrap_time = models.DateField(verbose_name=u"报废时间", null=True, blank=True)

    def __unicode__(self):
        if self.server_id.ipaddr:
            return self.server_id.ipaddr.ip_address
        return str(self.server_id.server_id)

    class Meta:
        verbose_name = u"生命周期"
        verbose_name_plural = u"生命周期管理表"


class RemoteInfo(models.Model):
    server_id = models.ForeignKey("Server", verbose_name=u"设备")
    connect_type = models.ForeignKey("ConnectType", verbose_name=u"连接方式")
    remote_username = models.CharField(verbose_name=u"远程连接用户", max_length=50, blank=True, null=True)
    remote_port = models.IntegerField(verbose_name=u"远程连接端口", blank=True, null=True)
    remote_password = models.CharField(verbose_name=u"远程连接密码", max_length=100, blank=True, null=True)
    enable_flag = models.BooleanField(verbose_name=u"远程连接启用开关", default=False)

    def __unicode__(self):
        if self.server_id.ipaddr:
            return self.server_id.ipaddr.ip_address
        return str(self.server_id.server_id)

    class Meta:
        verbose_name = u"远程连接信息"
        verbose_name_plural = u"远程连接信息表管理"


class ConnectType(models.Model):
    name = models.CharField(verbose_name=u"连接方式名称", max_length=100, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"连接方式"
        verbose_name_plural = u"连接方式管理表"


class ServerRecord(models.Model):
    pass


class Classify(models.Model):
    classify_name = models.CharField(verbose_name=u"分类名称", max_length=50, unique=True)

    def __unicode__(self):
        return self.classify_name

    class Meta:
        verbose_name = u"分类"
        verbose_name_plural = u"分类管理表"


class AttributeMap(models.Model):
    map_id = models.AutoField(verbose_name=u"映射表ID", primary_key=True)
    server_id = models.ForeignKey("Server", verbose_name=u"设备ID")
    attribute_id = models.ForeignKey("Attribute", verbose_name=u"属性")
    attribute_value_id = models.ForeignKey("AttributeValue", verbose_name=u"属性值")
    map_desc = models.CharField(verbose_name=u"映射表描述", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = u"属性映射表"
        verbose_name_plural = u"属性映射管理表"


class Attribute(models.Model):
    attribute_name = models.CharField(verbose_name=u"属性名称", max_length=100, unique=True)
    attribute_desc = models.CharField(verbose_name=u"属性名称描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.attribute_name

    class Meta:
        verbose_name = u"属性名称"
        verbose_name_plural = u"属性名称管理表"


class AttributeValue(models.Model):
    attribute_value = models.CharField(verbose_name=u"属性值", max_length=100, unique=True)
    attribute_value_desc = models.CharField(verbose_name=u"属性值描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.attribute_value

    class Meta:
        verbose_name = u"属性值"
        verbose_name_plural = u"属性值管理表"


class Person(models.Model):
    name = models.CharField(verbose_name=u"姓名", max_length=100, unique=True)
    email = models.EmailField(verbose_name=u"邮箱", blank=True, null=True)
    contact = models.CharField(verbose_name=u"联系方式", max_length=50, blank=True, null=True)
    department = models.CharField(verbose_name=u"部门", max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"责任人"
        verbose_name_plural = u"责任人管理表"