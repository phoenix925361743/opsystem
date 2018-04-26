#!/usr/bin/env python
# coding:utf-8

import socket
import urllib2
from install import initial_setting as ini


def start_udp_server(data):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create udp socket
    try:
        udp_socket.bind((ini.udp_server_ip, ini.udp_server_port),)  # bind the port with ip address
        print "start udp server: %s:%s" % (ini.udp_server_ip, ini.udp_server_port)
        while True:
            print "waitting for client send message..."
            client_data, address = udp_socket.recvfrom(1024)  # receive data from client
            if client_data == data:
                print "%s received, quit the udp server." % data
                break
            print "receive message %s, isn't the expect message" % client_data
        print "close the udp server socket"
        print address
        udp_socket.close()  # close socket
    except socket.error:
        print u"端口已被占用"
    return

if __name__ == "__main__":
    start_udp_server("192.168.18.100")


# import urllib2
# import json
# import socket
#
# port = 40123
# host = "192.168.19.36"
# url = "http://192.168.19.36/cobbler/listen/port/get/"
#
# request = urllib2.Request(url)
# response = urllib2.urlopen(request)



