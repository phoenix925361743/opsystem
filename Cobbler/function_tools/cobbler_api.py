#!/usr/bin/env python
# coding:utf-8

from install import initial_setting as ini
import xmlrpclib


class CobblerApi(object):
    """初始化处理cobbler接口，默认接收数据类型为字典，处理时会将字典的键和值都取出来给cobbler的api传递过去进行处理"""
    def __init__(self, data=None):
        self.username = ini.cobbler_username
        self.password = ini.cobbler_password
        self.cobbler_server = ini.cobbler_server
        self.data = data

    def initial(self):
        """初始化"""
        server = xmlrpclib.Server(self.cobbler_server)
        token = server.login(self.username, self.password)
        return server, token

    def get_system(self, system_name=None):
        """获取system，如果提供了system_name则获取指定system"""
        server, token = self.initial()
        if system_name:
            return server.get_item_handle("system", system_name, token)
        return server.get_systems()

    def system_modify(self, system_name=None):
        """修改system参数值"""
        server, token = self.initial()
        if system_name:  # 如果传递了system_name，则获取对应的system对象，如果没有，则创建一个新的system对象
            system = server.get_item_handle("system", system_name, token)
        else:
            system = server.new_system(token)
        for k in self.data.keys():  # 逐项修改或者添加对应的参数值
            server.modify_system(system, k, self.data.get(k), token)
        server.save_system(system, token)
        server.sync(token)
        return

    def get_profile(self, profile_name=None):
        """获取profile，如果提供了profile_name则获取指定profile"""
        server, token = self.initial()
        if profile_name:
            return server.get_item_handle("profile", profile_name, token)
        return server.get_profiles()

    def profile_modify(self, profile_name=None):
        """修改profile参数值"""
        server, token = self.initial()
        if profile_name:
            profile = server.get_item_handle("profile", profile_name, token)
        else:
            profile = server.new_profile(token)
        for k in self.data.keys():
            server.modify_profile(profile, k, self.data.get(k), token)
        server.save_profile(profile, token)
        server.sync(token)
        return

    def profile_remove(self, profile_name):
        """删除profile"""
        server, token = self.initial()
        server.remove_profile(profile_name, token)
        server.sync(token)
        return

    def get_distro(self, distro_name=None):
        """获取发行版本"""
        server, token = self.initial()
        if distro_name:
            return server.get_item_handle("distro", distro_name, token)
        return server.get_distros()






