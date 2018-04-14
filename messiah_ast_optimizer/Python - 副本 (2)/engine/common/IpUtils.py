# -*- coding:utf-8 -*-

import socket

def is_ipv4(ip):
    '\n\t\xe5\x88\xa4\xe6\x96\xad\xe4\xb8\x80\xe4\xb8\xaaip\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2\xe6\x98\xaf\xe4\xb8\x8d\xe6\x98\xaf\xe5\x90\x88\xe6\xb3\x95\xe7\x9a\x84ip\n\t'
    if (not isinstance(ip, str)):
        return False
    if ((len(ip) < 7) or (len(ip) > 15)):
        return False
    iplist = ip.split('.')
    if (len(iplist) != 4):
        return
    for ipstr in iplist:
        if (not ipstr.isdigit()):
            return False
        if ((int(ipstr) < 0) or (int(ipstr) > 255)):
            return False
    return True

def map_ipv4_to_ipv6(host, port=80):
    if (not is_ipv4(host)):
        return host
    flags = getattr(socket, 'AI_DEFAULT', socket.AI_ADDRCONFIG)
    addrinfos = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, flags)
    addrinfo = addrinfos[0]
    (family, socktype, proto, cannonname, sockaddr) = addrinfo
    return sockaddr[0]
