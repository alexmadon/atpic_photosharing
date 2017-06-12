#!/usr/bin/env python
# http://hg.nassrat.ca/ddb2/raw-file/ad64cd5b4f12/ddb2/ext_rep/yajl.py
'''
Script to parse json using yajl C library
'''

import sys
import traceback
from ctypes import *
from ctypes.util import find_library

YAJL_LIBRARY = find_library('yajl')
if not YAJL_LIBRARY:
    raise OSError('Cannot find libyajl in the system')
# libya
yajl = cdll.LoadLibrary(YAJL_LIBRARY)

# yajl = cdll.LoadLibrary('libyajl.so')

# from yajl_parse.h
class yajl_parser_config(Structure):
    _fields_ = [
        ("allowComments", c_uint),
        ("checkUTF8", c_uint)
    ]

# Callback Functions
YAJL_NULL = CFUNCTYPE(c_int, c_void_p)
YAJL_BOOL = CFUNCTYPE(c_int, c_void_p, c_int)
YAJL_INT  = CFUNCTYPE(c_int, c_void_p, c_longlong)
YAJL_DBL  = CFUNCTYPE(c_int, c_void_p, c_double)
YAJL_STR  = CFUNCTYPE(c_int, c_void_p, POINTER(c_ubyte), c_uint)
YAJL_SDCT = CFUNCTYPE(c_int, c_void_p)
YAJL_DCTK = CFUNCTYPE(c_int, c_void_p, POINTER(c_ubyte), c_uint)
YAJL_EDCT = CFUNCTYPE(c_int, c_void_p)
YAJL_SARR = CFUNCTYPE(c_int, c_void_p)
YAJL_EARR = CFUNCTYPE(c_int, c_void_p)

class yajl_callbacks(Structure):
    _fields_ = [
        ("yajl_null",           YAJL_NULL), 
        ("yajl_boolean",        YAJL_BOOL),
        ("yajl_integer",        YAJL_INT ),
        ("yajl_double",         YAJL_DBL ),
        ("yajl_string",         YAJL_STR ),
        ("yajl_start_map",      YAJL_SDCT),
        ("yajl_map_key",        YAJL_DCTK),
        ("yajl_end_map",        YAJL_EDCT),
        ("yajl_start_array",    YAJL_SARR),
        ("yajl_end_array",      YAJL_EARR),
    ]


# yajl_status
(
yajl_status_ok,
yajl_status_client_canceled,
yajl_status_insufficient_data,
yajl_status_error
) = map(c_int, xrange(4))

class YajlError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

class Yajl_Parser(object):
    '''
    A class that utilizes the Yajl C Library
    '''
    def __init__(self, c, buf_siz=65536):
        '''
        Takes a list of callback functions. The functions need to be in
        order and accepting the correct number of parameters, they
        should also reutrn an int. See yajl doc for more info on
        parameters and return values.
        '''
        c_funcs = ( 
            YAJL_NULL, YAJL_BOOL, YAJL_INT, YAJL_DBL, YAJL_STR,
            YAJL_SDCT, YAJL_DCTK, YAJL_EDCT, YAJL_SARR, YAJL_EARR
        )
        if len(c) != len(c_funcs):
            raise Exception("Must Pass %d Functions."%(len(c_funcs)))
        for i in range(10):
            c[i] = c_funcs[i](c[i])
        self.callbacks = yajl_callbacks(*c)
        self.buf_siz = buf_siz
        self.cfg = yajl_parser_config(1,1)
    
    def parse(self, f=sys.stdin, ctx=None): 
        '''Function to parse a JSON stream.
        Parameters:
        - f         : file stream to read from
        - buf_size  : size in bytes of read buffer
        - ctx       : A ctypes pointer that will be passed to all
                      callback functions as the first param
        '''
        hand = yajl.yajl_alloc( byref(self.callbacks), byref(self.cfg), ctx) 
        try:
            while 1:
                fileData = f.read(self.buf_siz-1)
                if not fileData:
                    break
                stat = yajl.yajl_parse(hand, fileData, len(fileData))
                if  stat != yajl_status_ok.value and \
                        stat != yajl_status_insufficient_data.value:
                    yajl.yajl_get_error.restype = c_char_p
                    error = yajl.yajl_get_error(hand, 1, fileData, len(fileData));
                    raise YajlError(error)
                    #yajl.yajl_free_error(error)
        except YajlError, inst:
            print(inst)
            print("This caused the parse to desist")
        except Exception, inst:
            print("An Error has Occured: %s"%inst)
            # traceback.print(_exception(*sys.exc_info()))
            # print( >>sys.stderr, "")
        yajl.yajl_free(hand)


# Sample callbacks, which print( invalid json)
# not to be used but rather to test the yajl parser

def yajl_null(ctx):
    print( "null")
    return 1

def yajl_boolean(ctx, boolVal):
    if boolVal:
        print( "true,")
    else:
        print( "false,")
    return 1

def yajl_integer(ctx, integerVal):
    print( "%s,"%integerVal)
    return 1

def yajl_double(ctx, doubleVal):
    print( "%s,"%doubleVal)
    return 1

def yajl_string(ctx, stringVal, stringLen):
    print( '"%s",'%string_at(stringVal, stringLen))
    return 1

def yajl_start_map(ctx):
    print( "{")
    return 1

def yajl_map_key(ctx, stringVal, stringLen):
    print( '"%s":'%string_at(stringVal, stringLen),)
    return 1

def yajl_end_map(ctx):
    print( "},")
    return 1

def yajl_start_array(ctx):
    print( "[")
    return 1

def yajl_end_array(ctx):
    print( "],")
    return 1


def main(args):
    callbacks = [
        yajl_null,
        yajl_boolean,
        yajl_integer,
        yajl_double,
        yajl_string,
        yajl_start_map,
        yajl_map_key,
        yajl_end_map,
        yajl_start_array,
        yajl_end_array
    ]
    parser = Yajl_Parser(callbacks)
    if args:
        for fn in args:
            f = open(fn)
            parser.parse(f=f)
            f.close()
    else:
        parser.parse()
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
