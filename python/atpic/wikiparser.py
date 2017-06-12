#!/usr/bin/python3
# python3.1 version
# uses pyparsing
# parses our special atpuc role in wiki restructured text


from pyparsing import *
import re
import atpic.log
import atpic.tokenizer
import atpic.mybytes

xx=atpic.log.setmod("INFO","wikiparser")

# http://rephrase.net/days/07/04/pyparsing
# http://crpppc19.epfl.ch/doc/python-pyparsing/htmldoc/frames.html

def parse(key):
    yy=atpic.log.setname(xx,'parse')
    atpic.log.debug(yy,'input=',key)
    id=Regex("[^@|:]+")("id") # non-space chars

    image=Literal("p:")+Optional(id('user')+Literal(':'))+id('image')+Optional(Literal('@')+id('resolution'))+Optional(Literal('|')('bar')+Optional(id)('link'))
    gallery=Literal("g:")+id('gallery')+Optional(Literal('|')+(image|id('link')))
    user=Literal("u:")+id('user')
    userdns=Literal("~")+id('userdns')
    internal=Literal("/")+id('internal')+Optional(Literal('|')+id('link'))
    wikipage=id("wikipage")+Optional(Literal('|')+id('link'))
    expr=image | gallery | user | userdns | internal | wikipage 
    result=expr.parseString(key)

    return result

def parse2array(key):
    yy=atpic.log.setname(xx,'parse2array')
    result=parse(key)
    atpic.log.debug(yy,)
    atpic.log.debug(yy,'++++++',key)
    atpic.log.debug(yy,key,'->',result)
    atpic.log.debug(yy,result.asXML())
    atpic.log.debug(yy,'---------')
    atpic.log.debug(yy,result.dump())
    atpic.log.debug(yy,'---------')
    atpic.log.debug(yy,'result.keys()=',result.keys())

    res={}
    # transforms into an array
    for akey in result.keys():
        res[akey]=result[akey]
    return res

if __name__ == "__main__":
    print('hi')
    keys=[
        'p:124', # display resolution @600 + title +link
        'p:1:124', # display resolution @600 + title +link PROHIBITED to cross user!!!!!!!!!, see SQL
        'p:124@r1024', # display resolution @1024 + title +link
        'p:124@r350', # display resolution @1024 + NO title +link
        'p:123|', # same with no link, really USEFUL????
        'p:123@r1024|', # same with no link, really USEFUL????
        'p:123|text link', # with text link
        'g:99' , # link to gallery 99
        'g:99|some text gallery' , # link to gallery 99
        '~alex', # dns or login? : dns, no SQL required, except if want to detect dead links
        'somewikipage', # no SQL required, except if want to detect dead links
        'somewikipage|some page', # 
        '/some/internal', # starts with slash
        '/some/internal|some internal', # starts with slash
        'u:1', # starts with slash
        'g:99|p:124' , # link to gallery 99 NOT GOOD 
        # NOT GOOD as same picid can move gallery
        'g:99|p:124@350' , # link to gallery 99 NOT GOOD
        ]
    for key in keys:
        print()
        print('++++++',key)
        result=parse2array(key)
        print('FINAL:',key,'==>',result)
