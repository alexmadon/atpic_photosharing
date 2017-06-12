#!/usr/bin/python3
# import logging
import atpic.log
import socket

xx=atpic.log.setmod("INFO","exiftool3k_client")




def recv_basic(the_socket):
    # http://code.activestate.com/recipes/408859-socketrecv-three-ways-to-turn-it-into-recvall/
    total_data=b''
    while True:
        data = the_socket.recv(8192)
        if not data: break
        total_data=total_data+data
    return total_data.decode('utf8')


def getexif(fname):
    # cf oreilley
    # Example 19-2. TCP echo client

    yy=atpic.log.setname(xx,'getexif')
    atpic.log.debug(yy,'doing %s' % fname)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 9999))
    
    fname=fname+"\n"
    sock.sendall(fname.encode('utf8'))
    response=recv_basic(sock)

    atpic.log.debug(yy,"Received: %s " % response)
    sock.close()
    return response

if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    getexif('TTTTTTTTttttt')
    getexif('/home/madon/public_html/perso/entreprise/sql_current/site/atpic/python/tests/fixture/raw/RAW_NIKON_D70.NEF')
