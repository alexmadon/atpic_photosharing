#!/usr/bin/python3
# ctyps wrapper to libyajl
# inspired by:
# http://pykler.github.com/yajl-py/
# libyajl2 - Yet Another JSON Library

# why?
# =========
# because i do not want to decode encode /decode encode
# similar to json.loads()

from atpic.jsonat_include import *
import atpic.log
import atpic.xmlob

xx=atpic.log.setmod("INFO","jsonat_json2python")


def parse(fileData):
    # this is the unction that is exposed and that should be used
    # it converts a bytes json string
    # to a bytes XML string

    # we define the stack variables in this function

    yy=atpic.log.setname(xx,'parse')

    # variables
    stack=[] # stores the (out,typ)


    def process_value(value):
        yy=atpic.log.setname(xx,"process_value")
        # atpic.log.debug(yy,'process_value',value)
        (res,typ)=stack.pop()
        if typ==b'array': # python list
            res.append(value)
            stack.append((res,typ))
        elif typ==b'key': # python hash array
            (res2,typ2)=stack.pop()
            res2[res]=value
            stack.append((res2,typ2))
        else:
            atpic.log.debug(yy,'WARNING!!!! unknown', (res,typ))

        atpic.log.debug(yy,stack)

    def update_stack_end():
        yy=atpic.log.setname(xx,"update_stack_end")
        atpic.log.debug(yy,'in',stack)
        if len(stack)>1:
            (out,typ)=stack.pop()
            (out2,typ2)=stack.pop()
            if typ2==b'key':
                (out3,typ3)=stack.pop()
                out3[out2]=out
                stack.append((out3,typ3))
            elif typ2==b'array':
                out2.append(out)
                stack.append((out2,typ2))

            else:
                atpic.log.debug(yy,'WARNING2!!!! unknown', (out2,typ2))
        else:
            atpic.log.debug(yy,'WARNING5 NOTHING TO DO')
        atpic.log.debug(yy,'out',stack)


    # implement the callbacks:

    def mynull(ctx):
        yy=atpic.log.setname(xx,"mynull")
        atpic.log.debug(yy,'mynull',ctx)
        value=None
        process_value(value)
        return 1
    
    def myboolean(ctx, boolVal):
        yy=atpic.log.setname(xx,"myboolean")
        atpic.log.debug(yy,'myboolean',ctx, boolVal)
        if boolVal==1:
            value=True
        else:
            value=False
        process_value(value)
        return 1

    def myinteger(ctx, integerVal):
        yy=atpic.log.setname(xx,"myinteger")
        atpic.log.debug(yy,'myinteger',ctx, integerVal)
        return 1

    def mydouble(ctx, doubleVal):
        yy=atpic.log.setname(xx,"mydouble")
        atpic.log.debug(yy,'mydouble',ctx, doubleVal)
        return 1

    def mynumber(ctx, stringVal, stringLen):
        yy=atpic.log.setname(xx,"mynumber")
        atpic.log.debug(yy,'mynumber',ctx, stringVal, stringLen)
        value=string_at(stringVal, stringLen)
        atpic.log.debug(yy,'value',value)
        process_value(value)
        return 1

    def mystring(ctx, stringVal, stringLen):
        yy=atpic.log.setname(xx,"mystring")
        atpic.log.debug(yy,'mystring',ctx, stringVal, stringLen) # use ctypes string_at
        value=string_at(stringVal, stringLen)
        atpic.log.debug(yy,'value',value)
        process_value(value)
        return 1

    def mymap_key(ctx, stringVal, stringLen):
        yy=atpic.log.setname(xx,"mymap_key")
        atpic.log.debug(yy,'mymap_key',ctx, stringVal, stringLen)
        key=string_at(stringVal, stringLen)
        atpic.log.debug(yy,'key',key)
        stack.append((key,b'key'))
        atpic.log.debug(yy,'stack',stack)
        return 1

    def mystart_map(ctx):
        yy=atpic.log.setname(xx,"mystart_map")
        atpic.log.debug(yy,'mystart_map',ctx)
        out={}
        stack.append((out,b'map'))
        atpic.log.debug(yy,'stack',stack)
        return 1
    
    def myend_map(ctx):
        yy=atpic.log.setname(xx,"myend_map")
        atpic.log.debug(yy,'myend_map',ctx,'++++++++++++++++++++++++++++++++')
        update_stack_end()
        atpic.log.debug(yy,'stackmapout',stack)
        return 1
        
    def mystart_array(ctx):
        yy=atpic.log.setname(xx,"mystart_array")
        atpic.log.debug(yy,'mystart_array',ctx)
        out=list()
        stack.append((out,b'array'))
        atpic.log.debug(yy,'stack',stack)
        return 1

    def myend_array(ctx):
        yy=atpic.log.setname(xx,"myend_array")
        atpic.log.debug(yy,'myend_array',ctx)
        atpic.log.debug(yy,'in',stack)
        update_stack_end()
        atpic.log.debug(yy,'out',stack)
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

    (out,typ)=stack.pop()
    atpic.log.debug(yy,'will return',out)
    return out
    # return stack
        
if __name__ == "__main__":
    print("testing json")
    jsons=[
        b'{"key1" : ["val1a","val1b"], "key2" : "val2"}',
        b'{"first":"alex","second":"madon","first":"john"}',
        b'[["first","alex"],["second","madon"],["first","john"]]',
        ]
    for json in jsons:
        print('input=',json)
        ss=parse(json)
        print('output=',ss)
