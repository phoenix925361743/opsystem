#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
from django import forms


class SshInfo(forms.Form):
    ssh_ipaddr = forms.CharField(label=u"远程连接地址", max_length=30)
    ssh_port = forms.IntegerField(label=u"远程连接端口")
    ssh_user = forms.CharField(label=u"远程连接用户", max_length=30)
    ssh_passwd = forms.CharField(label=u"远程连接密码", max_length=50)


class SshFileUpload(forms.Form):
    files = forms.FileField(label=u"CSV上传")

    def clean_file(self):
        #  清洗上传文件，同时判断扩展名是否为csv
        data = self.cleaned_data["files"]
        file_name_suffix = os.path.splitext(data.name)[1].lower()  # 获取上传文件的后缀名
        if file_name_suffix != '.csv':
            raise forms.ValidationError(u"请上传csv格式文件！")
        return data
