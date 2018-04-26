# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from UserAccess.function_tools.salt_encrypt import salt_encrypt


class MyUser(models.Model):
    username = models.CharField(verbose_name=u"用户名", max_length=100, unique=True)
    password = models.CharField(verbose_name=u"密码", max_length=100)
    email = models.EmailField(verbose_name=u"邮箱", unique=True)
    depart = models.ForeignKey("Department", verbose_name="部门")
    role = models.ManyToManyField("Roles", verbose_name=u"角色")
    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=timezone.now)
    modify_time = models.DateTimeField(verbose_name=u"修改时间", auto_now=timezone.now)
    use = models.BooleanField(verbose_name=u"启用状态", default=False)

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        # if self.username == "admin":  # 同步修改admin账号的密码
        #     from django.contrib.auth.models import User
        #     from django.db.utils import IntegrityError
        #     try:
        #         User.objects.filter(username="admin").update(password=self.password)
        #     except IntegrityError:
        #         pass
        if not len(self.password) == 32:    # 由于前端密码长度限制为6~15，hash加密后密码为32位，此处判断密码长度不为32位时才进行hash加密
            self.password = salt_encrypt(self.email, self.password)
        super(MyUser, self).save(*args, **kwargs)
        return

    class Meta:
        verbose_name = u"用户"
        verbose_name_plural = u"用户管理"


class UserGroup(models.Model):
    group_name = models.CharField(verbose_name=u"组名称", max_length=100, unique=True)
    group_user = models.ManyToManyField("MyUser", verbose_name=u"组成员")
    group_permission = models.ManyToManyField("Permission", verbose_name=u"组权限")
    group_desc = models.TextField(verbose_name=u"组描述", blank=True, null=True)
    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=timezone.now)
    modify_time = models.DateTimeField(verbose_name=u"修改时间", auto_now=timezone.now)

    def __unicode__(self):
        return self.group_name

    class Meta:
        verbose_name_plural = u"用户组管理"
        verbose_name = u"用户组"


class Department(models.Model):
    """部门管理表"""
    depart = models.CharField(verbose_name=u"部门名称", max_length=200, unique=True)
    desc = models.TextField(verbose_name=u"部门简介", blank=True, null=True)

    def __unicode__(self):
        return self.depart

    class Meta:
        verbose_name_plural = u"部门管理"
        verbose_name = u"部门"


class Roles(models.Model):
    role_name = models.CharField(verbose_name=u"角色名称", max_length=20, unique=True)
    permission = models.ManyToManyField("Permission", verbose_name=u"角色权限", blank=True)
    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=timezone.now)
    modify_time = models.DateTimeField(verbose_name=u"修改时间", auto_now=timezone.now)

    def __unicode__(self):
        return self.role_name

    class Meta:
        verbose_name = u"角色"
        verbose_name_plural = u"角色管理"


class Permission(models.Model):
    permission_name = models.CharField(verbose_name=u"权限名称", max_length=50, unique=True)
    permission_value = models.CharField(verbose_name=u"权限属性", max_length=50, unique=True)
    permission_detail = models.TextField(verbose_name=u"权限描述", blank=True, null=True)
    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=timezone.now)
    modify_time = models.DateTimeField(verbose_name=u"修改时间", auto_now=timezone.now)

    def __unicode__(self):
        return self.permission_value + r" | " + self.permission_name

    class Meta:
        verbose_name = u"权限"
        verbose_name_plural = u"权限管理"


class LoginRecord(models.Model):
    login_user = models.ForeignKey("MyUser", verbose_name="登录用户")
    login_ip = models.CharField(verbose_name=u"登录IP", max_length=50)
    login_time = models.DateTimeField(verbose_name=u"登录时间", null=True, blank=True)
    login_exit_time = models.DateTimeField(verbose_name=u"退出时间", null=True, blank=True)

    def __unicode__(self):
        return self.login_user.username

    def save(self, *args, **kwargs):
        record_set = LoginRecord.objects.filter(login_user=self.login_user)
        record_num = len(record_set)
        if record_num > 9:
            record_set[record_num-1].delete()
        super(LoginRecord, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"登录记录"
        verbose_name_plural = u"登录记录管理"
        ordering = ["-login_time"]


def image_filepath(instance, filename):
    """
    格式化图片上传的路径名称。
    :param instance:
    :param filename:
    :return:
    """
    return "avatar/%s/%s" % (instance.user, filename)


class UserProfile(models.Model):
    user = models.OneToOneField("MyUser", verbose_name=u"所属用户")
    introduce = models.CharField(verbose_name=u"个人简介", max_length=500, blank=True, null=True)
    phone = models.IntegerField(verbose_name=u"联系电话", null=True, blank=True)
    avatar = models.ImageField(verbose_name=u"头像", upload_to=image_filepath, default="avatar/default/default.png")

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = u"用户配置"
        verbose_name_plural = u"用户配置管理"