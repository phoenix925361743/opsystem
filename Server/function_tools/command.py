#!/usr/bin/env python
# _*_ coding:utf-8 _*_


"""
shell命令默认以centos为准，同时需要被查询机器安装有dmidecode，否则查询结果将为空。
"""


shell_command_dict = {
    "service_sn": "dmidecode -t system | grep -i 'serial number' | cut -d ':' -f2",
    "service_manufacturer": "dmidecode -t system | grep -i 'manufacturer' | cut -d ':' -f2",
    "service_product_name": "dmidecode -t system | grep -i 'product name' | cut -d ':' -f2",
    "service_cpu": "cat /proc/cpuinfo | grep -i 'model name' | head -1 | cut -d ':' -f2",
    "service_memory": "free -m|grep -i 'mem' | awk '{print $2}'",
    "service_os": "rpm -q centos-release",
}