#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import paramiko


class SSHResolve(object):
    """
    通过paramiko创建ssh连接，并执行命令获取输出结果;
    :param:host:连接主机名;
    :param:port:连接端口;
    :param:user:连接用户;
    :param:passwd:连接密码;
    :param:command:等待执行的命令集，字典类型，其中字典的key为命令获取结果的变量名，字典的value为获取该结果的命令。
    """
    def __init__(self, host, port, user, passwd, command):
        self.host = host
        self.port = int(port)
        self.user = user
        self.passwd = passwd
        self.command = command
        self.data = {}

    def create_connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.host, self.port, self.user, self.passwd, timeout=5)  # 创建ssh连接，并设置超时时间为6秒
        except paramiko.AuthenticationException:
            return None
        return ssh

    def executed_command(self):
        ssh_connect = self.create_connect()
        if ssh_connect:
            for key, value in self.command.items():
                stdin, stdout, stderr = ssh_connect.exec_command(value)
                self.data[key] = stdout.read()
            ssh_connect.close()
            self.data["connect"] = True
        else:
            self.data["connect"] = False
        return self.data




