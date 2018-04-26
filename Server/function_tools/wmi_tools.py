#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import wmi


class WmiTools(object):
    """
    查询windows官方wmi接口之后，结合查询对比结果，发现很多提供的接口，在部分设备上可以取到数据，而在部分设备上取不到数据，
    这直接导致的结果是统计过程将会变得很复杂，so，
    暂时停止这种做法。
    """
    def __init__(self, computer, user, password):
        self.computer = computer
        self.user = user
        self.password = password
        self.system_info = {}
        self.disk_info = {}

    def connect_create(self):
        conn = wmi.WMI(computer=self.computer, user=self.user, password=self.password)
        return conn

    def get_system_info(self):
        c = self.connect_create()
        try:
            for disk in c.Win32_DiskDrive():
                s_number = 1
                key = "disk" + str(s_number)
                self.disk_info[key + "_type"] = disk.Capation               # 获取每一块硬盘的型号;
                self.disk_info[key + "_size"] = int(disk.Size) / 1024 ** 3  # 获取每一块硬盘的大小，单位MB;
                self.disk_info[key + "_sn"] = disk.SerialNumber.split()[0]  # 获取每一块硬盘的序列号;
                s_number += 1
            self.system_info["disk_info"] = self.disk_info
            self.system_info["cpu_caption"] = c.Win32_Processor()[0].Caption
        except:
            self.system_info["message"] = "something is wrong"
        return self.system_info
