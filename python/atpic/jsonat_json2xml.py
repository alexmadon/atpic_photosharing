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


def parse(fileData,firstElement=b'DOC'):
    # this is the unction that is exposed and that should be used
    # it converts a bytes json string
    # to a bytes XML string

    # we define the stack variables in this function

    yy=atpic.log.setname(xx,'parse')

    # variables
    stack=[]
    stack.append((b'm',b'DOC')) # type: Map, Key:DOC
    out=[]
    
    def process_value(value):
        (t,k)=stack.pop()
        if t==b'k': # key
            atpic.log.debug(yy,'AAAA')
            out.append(b'<'+k+b'>')
            out.append(value)
            out.append(b'</'+k+b'>')
        elif t==b'm': # map
            atpic.log.debug(yy,'BBBB')
            pass
        elif t==b'a': # array
            atpic.log.debug(yy,'CCCC')
            out.append(b'<'+k+b'>')
            out.append(value)
            out.append(b'</'+k+b'>')
            stack.append((t,k))

    # implement the callbacks:

    def mynull(ctx):
        atpic.log.debug(yy,'mynull',ctx)
        return 1
    
    def myboolean(ctx, boolVal):
        atpic.log.debug(yy,'myboolean',ctx, boolVal)
        if boolVal:
            value=b'True'
        else:
            value=b'False'
        process_value(value)
        return 1

    def myinteger(ctx, integerVal):
        atpic.log.debug(yy,'myinteger',ctx, integerVal)
        return 1

    def mydouble(ctx, doubleVal):
        atpic.log.debug(yy,'mydouble',ctx, doubleVal)
        return 1

    def mynumber(ctx, stringVal, stringLen):
        atpic.log.debug(yy,'mynumber',ctx, stringVal, stringLen)
        atpic.log.debug(yy,string_at(stringVal, stringLen))
        value=string_at(stringVal, stringLen)
        process_value(value)
        return 1

    def mystring(ctx, stringVal, stringLen):
        atpic.log.debug(yy,'mystring',ctx, stringVal, stringLen) # use ctypes string_at
        atpic.log.debug(yy,string_at(stringVal, stringLen))
        value=string_at(stringVal, stringLen)
        atpic.log.debug(yy,stack)
        process_value(value)
        return 1

    def mymap_key(ctx, stringVal, stringLen):
        atpic.log.debug(yy,'mymap_key',ctx, stringVal, stringLen)
        atpic.log.debug(yy,string_at(stringVal, stringLen))
        atpic.log.debug(yy,stack)
        key=string_at(stringVal, stringLen)
        stack.append((b'k',key)) # key
        return 1

    def mystart_map(ctx):
        atpic.log.debug(yy,'mystart_map',ctx)
        atpic.log.debug(yy,stack)
        (t,k)=stack.pop()
        atpic.log.debug(yy, "(t,k)", (t,k))
        out.append(b'<'+k+b'>')
        stack.append((t,k))
        return 1
    
    def myend_map(ctx):
        atpic.log.debug(yy,'myend_map',ctx,'++++++++++++++++++++++++++++++++')
        atpic.log.debug(yy,stack)
        (t,k)=stack.pop()
        atpic.log.debug(yy, "(t,k)", (t,k))
        out.append(b'</'+k+b'>')
        if t==b'a':
            stack.append((t,k))
        return 1
        
    def mystart_array(ctx):
        atpic.log.debug(yy,'mystart_array',ctx)
        atpic.log.debug(yy,stack)
        (t,k)=stack.pop()
        stack.append((b'a',k))
        return 1

    def myend_array(ctx):
        atpic.log.debug(yy,'myend_array',ctx)
        atpic.log.debug(yy,stack)
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
        atpic.log.debug(yy,'stat',stat)
        atpic.log.debug(yy,yajl_status_ok.value)
        if stat != yajl_status_ok.value:
            yajl.yajl_get_error.restype = c_char_p
            error = yajl.yajl_get_error(hand, 1, fileData, len(fileData))
            atpic.log.debug(yy,'error:',error.decode('utf8'))
        # need to clean even if there are exception
        yajl.yajl_free(hand)

    myparse(fileData)
    ss=b''.join(out)
    return ss

        
if __name__ == "__main__":
    print("testing json")
    json=b'{"key1" : ["val1a","val1b"], "key2" : "val2"}'
    print('input=',json.decode('utf8'))
    ss=parse(json)
    print('output=',ss.decode('utf8'))
