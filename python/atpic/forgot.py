#!/usr/bin/python3


"""
If user forgot his password,
but remembers
- his UID
- his email
- his login
we can send an email
with a link that has a session
to a reset password page

session is encrypted random+login+time (session is valid only for X minutes)

GET http://atpic.com/forgot (presents a form)
POST http://atpic.com/forgot (sends a mail with a session, tell to check spam box)
GET http://atpic.com/reset/xyzzzzzzzz (presents a from to reset passwd if session is valid, reminds the login)
POST http://atpic.com/reset/xyzzzzzzz (check session again,check both passwd are same, updates the passwd and if successful, presents login form)


"""
import atpic.log

xx=atpic.log.setmod("INFO","forgot")

"""
NOT USED ANYMORE, just do sendmail.postprocessing

def get_fnamevalue(indata):
    fieldname=b''
    fieldvalue=b''
    for (fname,isfile,fvalue) in indata:
        if fname==b'fieldname':
            fieldname=fvalue
        elif fname==b'fieldvalue':
            fieldvalue=fvalue
    return (fieldname,fieldvalue)
"""


"""
NOT USED ANYMORE, just do sendmail.postprocessing

def work_xml_forgot(db,actions,indata,xmlo):
    yy=atpic.log.setname(xx,'work_xml_forgot')
    atpic.log.debug(yy,'input=',(db,actions,indata,xmlo.data.content))
    if actions[0]==b'get':
        xmlo.data.append(b'<forgot/>')
    elif actions[0]==b'post':
        xmlo.data.append(b'<forgot/>')
        (fieldname,fieldvalue)=get_fnamevalue(indata)
        if fieldname in [b'id',b'_email',b'_servershort']:
            atpic.log.debug(yy,'need to lookup in DB')
        else:
            atpic.log.error(yy,'fieldname',fieldname,'unknown')

    atpic.log.debug(yy,'output=',b''.join(xmlo.data.content))

    return xmlo

"""

if __name__ == "__main__":
    print('hi')
    indata=[(b'fieldname', False, b'uid'), (b'fieldvalue', False, b'1')]
    print(get_fnamevalue(indata))
