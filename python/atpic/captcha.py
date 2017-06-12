#!/usr/bin/python3
"""
Idea:
we store in Redis a string:
captcha_publickeyaaaasssss:RGTHY with alife of 10 minutes
at each form display

When the form is submitted: 
if the key is present: we process that form and we remove that key
(so that the key can be used only once)
if the key is not present: we stop

Danger: could fill the memory with captchas...

Other possible alo: do not store anything;
Danger: do not know if it hase been used.
To mark as 'used', would need to store in memory, hence same danger as above.

Could rate limit at form submission, but can also rate limit at captcha image 
generation.

"""
# see php: spit_challenge_image
# http://code.google.com/p/django-simple-captcha/
# flite
# https://github.com/mbi/django-simple-captcha

import random
import traceback
import subprocess

import atpic.indatautils
from atpic.redisconst import *
from atpic.mybytes import *
import atpic.log

xx=atpic.log.setmod("INFO","captcha")

def spit_image(challenge):
    challenge=challenge.decode('utf8')
    yy=atpic.log.setname(xx,'spit_image')
    size=random.randint(20,40);
    stroke=size/15;
    command=[]
    command.append("convert")
    command.append("-pointsize")
    command.append("%s" % size)
    command.append("label:%s" % challenge)
    command.append("-background")
    command.append("white")
    command.append("-fill")
    command.append("black")  
    command.append("-stroke") 
    command.append("black")  
    command.append("-strokewidth")
    command.append("%s" % stroke)
    for i in [0,1]:
        high1=random.randint(0,size)
        command.append("-draw")
        command.append("stroke-opacity 1      path 'M 0,%s L 1000,%s'" % (high1,high1))
    command.append("-wave")
    command.append("5x40")
    command.append("-wave")
    command.append("5x300")
    command.append("-rotate")
    command.append("%s" % random.randint(-50,50))
    command.append("png:-")
    # print(command)
    acommand=''.join(command)
    output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]   
    return output
    # header("Content-Type: image/png");
    

def captcha_protected_url(hxplo,pxplo,actions):
    """
    Checks if URL should be captcah protected
    and if it is, give the data xpath
    It is the VERY EASY to protect new forms: just modify the function.
    This can be unit tested.
    """
    yy=atpic.log.setname(xx,'captcha_protected_url')
    atpic.log.debug(yy,'input=',hxplo,pxplo,actions)
    protected=False
    xpath=b''
    if hxplo.list()==[(b'atpiccom',None),]:
        atpic.log.debug(yy,'we are atpiccom')
        if pxplo.list()==[(b'user', None),]:
            atpic.log.debug(yy,'we are user')
            protected=True
            xpath=b'/user'
        elif pxplo.list()==[(b'forgot', None),]:
            atpic.log.debug(yy,'we are in forgot')
            protected=True
            xpath=b'/forgot'



    atpic.log.debug(yy,'output=',protected,xpath)
    return (protected,xpath)
# add the captchahidden and captchapublic in PRE or POST PROCESSING?
# captcha_hidden and captcha_public

# most logical is in POST PROCESSING to display get forms
# /notok/post/post/user
# /ok/get/post/user
def need_captcha_postprocessing(rediscon,dataerror,hxplo,pxplo,actions,xmlo):
    # base the decision on url and dataerror
    yy=atpic.log.setname(xx,'need_captcha_postprocessing')
    atpic.log.debug(yy,'input=',rediscon,dataerror,hxplo,pxplo,actions,xmlo)
    need=False
    xpath=b''
    if actions == [b'get',b'post'] or ( (actions == [b'post'] or actions == [b'post', b'post']) and dataerror ):
        (protected,xpath)=captcha_protected_url(hxplo,pxplo,actions)
        if protected:
            need=True

    atpic.log.debug(yy,'output=',need)
    return (need,xpath)

def postprocessing(rediscon,dataerror,hxplo,pxplo,actions,xmlo):
    # insert (/ok/get/post/user) or
    # replace (/notok/post/post/user) 
    # the two captcha fields captchahidden (blank) and captchapublic (newkey)
    # while storing in Redis the (public,hidden) pair
    yy=atpic.log.setname(xx,'postprocessing')
    atpic.log.debug(yy,'input',rediscon,dataerror,hxplo,pxplo,actions,xmlo)
    (need,xpath)=need_captcha_postprocessing(rediscon,dataerror,hxplo,pxplo,actions,xmlo)
    atpic.log.debug(yy,'need,xpath',need,xpath)
    if need:
        xml_string=b''.join(xmlo.data.content)
        atpic.log.debug(yy,'xml_string=',xml_string)
        basepath=xpath
        # captchahidden=b'somehidden'
        # captchapublic=b'somepublic'
        publen=30 # 30digits on public key
        captchapublic=random.randint(pow(10,publen),pow(10,publen+1)-1)
        captchapublic=int2bytes(captchapublic)
        hidlen=4 # 
        captchahidden=random.randint(pow(10,hidlen),pow(10,hidlen+1)-1)
        captchahidden=int2bytes(captchahidden)
        atpic.log.debug(yy,'will set',captchapublic,captchahidden)
        atpic.redis_pie._set(rediscon,REDIS_CAPTCHA+captchapublic,captchahidden)
        atpic.redis_pie._expire(rediscon,REDIS_CAPTCHA+captchapublic,b'300') # store captcha only for 5 minutes
        anarray={b'captchahidden':b'',b'captchapublic':captchapublic}
        xml_string=atpic.xmlutils.replace_params(xml_string,basepath,anarray)
        # update the XML with what we have found
        xmlo.data.content=[xml_string,]
        xmlo.data.stack=[]
    atpic.log.debug(yy,'output=',xmlo)
    return xmlo
    

def need_captcha_preprocessing(indata,hxplo,pxplo,actions,environ):
    # need to see in pre processing a valid captcha
    # if post or post,post user
    yy=atpic.log.setname(xx,'need_captcha_preprocessing')
    atpic.log.debug(yy,'input=',indata,hxplo,pxplo,actions,environ)
    need=False
    xpath=b''
    if actions == [b'post'] or actions == [b'post',b'post']:
        (protected,xpath)=captcha_protected_url(hxplo,pxplo,actions)
        if protected:
            need=True

    atpic.log.debug(yy,'output=',need)
    return need

# most logical in PRE PROCESSING for POST
# because at POST time you will need 
# 1) check it before SQL
# 2) to clean it before sending to SQL
def preprocessing(rediscon,indata,dataerror,hxplo,pxplo,actions,environ):
    # check there is a captchahidden  and captchapublic
    # and if there is: check in Redis the hidden correspond to the public
    # on error raise an exception to avoid storing in SQL
    # but present a new captcha (see postprocessing)
    yy=atpic.log.setname(xx,'preprocessing')
    atpic.log.debug(yy,'input=',(rediscon,indata,dataerror,hxplo,pxplo,actions,environ))
    captchaerrors=[]
    error=False
    if need_captcha_preprocessing(indata,hxplo,pxplo,actions,environ):
        try:
            captchapublic=atpic.indatautils.get(indata,b'captchapublic',b'')
            atpic.log.debug(yy,'captchapublic',captchapublic,)
            captchahidden=atpic.indatautils.get(indata,b'captchahidden',b'')
            atpic.log.debug(yy,'captchahidden',captchahidden)
            captcha_hidden_redis=atpic.redis_pie._get(rediscon,REDIS_CAPTCHA+captchapublic)
            atpic.log.debug(yy,'captchahidden_redis',captcha_hidden_redis)
            if len(captcha_hidden_redis)>1 and captcha_hidden_redis==captchahidden:
                atpic.log.debug(yy,'good captcha')
                # need to clean the captcha as it is use once
                atpic.redis_pie._del(rediscon,REDIS_CAPTCHA+captchapublic)
            else:
                atpic.log.debug(yy,'bad captcha')
                dataerror[b'captchahidden']=[b'bad captcha']
        except:
            atpic.log.error(yy,traceback.format_exc())
            dataerror[b'captchahidden']=[b'captcha error']
    # if error post precessing will regenerate and captcha
    atpic.log.debug(yy,'output=',indata,dataerror)
    return (indata,dataerror)

if __name__ == "__main__":
    
    output=spit_image("ABDC")
    print(output)
