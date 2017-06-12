#!/usr/bin/python3
import socket
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]  

def get_islocal():
    myip=get_ip_address()
    print(myip)
    if myip.startswith('192.168'):
        res=True
    else:
        res=False
    return res

if __name__ == "__main__":
    print(get_ip_address())
    print(get_islocal())
