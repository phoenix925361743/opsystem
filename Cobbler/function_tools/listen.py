#!/usr/bin/env python
# coding:utf-8

from multiprocessing import Process, Queue
from time import sleep
import os


def ping_task(ip):
    command = "ping -c 3 -q %s" % ip
    code = 1
    while code != 0:
        code = os.system(command)
    return





