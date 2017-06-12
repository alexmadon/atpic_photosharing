# those are the config parameters
import  atpic.whatismyip

def get_readonly():
    # returns True is system is in read-only mode
    # returns false if system is in read-write mode
    return False

def get_tld(environ):
    server_addr=environ.get(b'SERVER_ADDR',b'')
    # if server_addr==b'127.0.0.1':
    #     tld=b'.faa'
    # else:
    #     tld=b'.foo'
    host=environ.get(b'HTTP_HOST',b'')
    if host.endswith(b'com'):
        tld=b'.com'
    else:
        tld=b'.faa'
    return tld


def get_islocal():
    # function based on IP
    # returns True is at home, false if on the internet (production)
    islocal=atpic.whatismyip.get_islocal()
    return islocal

def get_defaultip():
    return b'5.9.136.58'

def get_defaultpartition():
    return b'b'


def remove_tmp_files():
    # equivalent of nginx "client_body_in_file_only clean|on|off;"
    # can be set to False to debug
    # should typically be set to True
    return False
