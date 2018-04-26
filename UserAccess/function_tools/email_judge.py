#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import socket


def email_judge(email):
    """
    验证邮箱地址是否满足正常的邮箱地址格式，以及是否可用。
    :param email:
    :return:
    """
    email_part = email.split("@")
    if len(email_part) == 2:
        try:
            socket.getaddrinfo(email_part[-1], None)
            return True
        except socket.gaierror:
            return False
    return False
