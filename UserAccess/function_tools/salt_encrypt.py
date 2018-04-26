#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import hashlib


def salt_encrypt(email, raw_password):
    """
    加密用户的密码，salt为用户的邮箱，保证即使密码一样，也不可能出现相同的加密密码。
    :param email: 一个邮箱字符串。
    :param raw_password:原始密码。
    :return:返回一个加密后的密码字符串的md5。
    """
    hashs = hashlib.md5()
    salt_str = email + raw_password
    hashs.update(salt_str)
    encrypt_password = hashs.hexdigest()
    return encrypt_password
