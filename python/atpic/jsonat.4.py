#!/usr/bin/python3
# ctyps wrapper to libyajl
# inspired by:
# http://pykler.github.com/yajl-py/
# libyajl2 - Yet Another JSON Library

# why?
# =========
# because i do not want to decode encode /decode encode
# because It could convert directly to XML

from atpic.jsonat_include import *
import atpic.log
import atpic.xmlob

xx=atpic.log.setmod("INFO","jsonat")

def prunt(*args):
    print(*args)
    pass

def prant(*args):
    print(*args)
    pass


stack=[]
stack.append((b'm',b'DOC')) # type: Map, Key:DOC
out=[]

def process_value(value):
    (t,k)=stack.pop()
    if t==b'k':
        print('AAAA')
        out.append(b'<'+t+k+b'>')
        out.append(value)
        out.append(b'</'+t+k+b'>')
    elif t==b'm': # map
        print('BBBB')
        pass
    elif t==b'a': # array
        print('CCCC')
        out.append(b'<'+t+k+b'>')
        out.append(value)
        out.append(b'</'+t+k+b'>')
        stack.append((t,k))

# implement the callbacks:


def mynull(ctx):
    prant('mynull',ctx)
    return 1

def myboolean(ctx, boolVal):
    prant('myboolean',ctx, boolVal)
    if boolVal:
        value=b'True'
    else:
        value=b'False'
    process_value(value)
    return 1

def myinteger(ctx, integerVal):
    prant('myinteger',ctx, integerVal)
    return 1

def mydouble(ctx, doubleVal):
    prant('mydouble',ctx, doubleVal)
    return 1

def mynumber(ctx, stringVal, stringLen):
    prant('mynumber',ctx, stringVal, stringLen)
    prant(string_at(stringVal, stringLen))
    value=string_at(stringVal, stringLen)
    process_value(value)
    return 1

def mystring(ctx, stringVal, stringLen):
    prant('mystring',ctx, stringVal, stringLen) # use ctypes string_at
    prant(string_at(stringVal, stringLen))
    value=string_at(stringVal, stringLen)
    prant(stack)
    process_value(value)
    return 1

def mymap_key(ctx, stringVal, stringLen):
    prant('mymap_key',ctx, stringVal, stringLen)
    prant(string_at(stringVal, stringLen))
    prant(stack)
    key=string_at(stringVal, stringLen)
    stack.append((b'k',key))
    return 1

def mystart_map(ctx):
    prant('mystart_map',ctx)
    prant(stack)
    (t,k)=stack.pop()
    print( "(t,k)", (t,k))
    out.append(b'<'+t+k+b'>')
    stack.append((t,k))
    return 1

def myend_map(ctx):
    prant('myend_map',ctx,'++++++++++++++++++++++++++++++++')
    prant(stack)
    (t,k)=stack.pop()
    print( "(t,k)", (t,k))
    out.append(b'</'+t+k+b'>')
    if t==b'a':
        stack.append((t,k))
    return 1

def mystart_array(ctx):
    prant('mystart_array',ctx)
    prant(stack)
    (t,k)=stack.pop()
    stack.append((b'a',k))
    return 1

def myend_array(ctx):
    prant('myend_array',ctx)
    prant(stack)
    (t,k)=stack.pop()
    return 1





# 
yajl_callbks = yajl_callbacks() # create a structure

# implement some prototypes
yajl_callbks.yajl_null=YAJL_NULL(mynull)
yajl_callbks.yajl_boolean=YAJL_BOOL(myboolean)
# yajl_callbks.yajl_integer=YAJL_INT(myinteger)
# yajl_callbks.yajl_double=YAJL_DBL(mydouble)
yajl_callbks.yajl_number=YAJL_NUM(mynumber) # one or the two other: yajl_integer and yajl_double
yajl_callbks.yajl_string=YAJL_STR(mystring)
yajl_callbks.yajl_start_map=YAJL_SDCT(mystart_map)
yajl_callbks.yajl_map_key=YAJL_DCTK(mymap_key)
yajl_callbks.yajl_end_map=YAJL_EDCT(myend_map)
yajl_callbks.yajl_start_array=YAJL_SARR(mystart_array)
yajl_callbks.yajl_end_array=YAJL_EARR(myend_array)

def myparse(fileData):
    hand = yajl.yajl_alloc(byref(yajl_callbks),None,None)
    stat=yajl.yajl_parse(hand, fileData, len(fileData))
    print('stat',stat)
    print(yajl_status_ok.value)
    if stat != yajl_status_ok.value:
        yajl.yajl_get_error.restype = c_char_p
        error = yajl.yajl_get_error(hand, 1, fileData, len(fileData))
        print('error:',error.decode('utf8'))
    # need to clean even if there are exception
    yajl.yajl_free(hand)
        
if __name__ == "__main__":
    print("testing json")
    fileData=b'{"key1" : ["val1a","val1b"], "key2" : "val2"}'
    myparse(fileData)


    ss=b''.join(out)
    print(ss.decode('utf8'))
    # print('xmle.stack',xmle.stack)
    print(fileData.decode('utf8'))
