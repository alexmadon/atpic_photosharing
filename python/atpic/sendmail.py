#! /usr/bin/python3

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import os
import traceback
from lxml import etree
import io
import time
import ssl

import atpic.log
import atpic.authenticatecrypto
import atpic.mybytes
import atpic.whatismyip

"""
Our servers are able to send mail (postfix installed)
But we use postfix only for large mailing lists (limits in the nb of recipients on gmail)

For one mail, we try google as more reliable and as functionality is critical. Traffic expected is rather low. May need to switch to our servers if traffic increases (limits on gmail?)

"""

xx=atpic.log.setmod("INFO","sendmail")


def create_data(mail_subject,mail_html):
    """
    Utility to create the STMP DATA
    """
    yy=atpic.log.setname(xx,'create_data')
    atpic.log.debug(yy,'input=',(mail_subject,mail_html))
    msg = MIMEMultipart('related')
    msg['Subject'] = Header(mail_subject.decode('utf8'),'utf-8')
    msg['From'] = '"Atpic Version2" <atpicversion2@gmail.com>'
    
    # attach the HTML
    part2 = MIMEText(mail_html.decode('utf8'), 'html','utf-8')
    msg.attach(part2)

    # attach an image
    # 
    #        fp = open(dirname+'/'+attachment, 'rb')
    #        img = MIMEImage(fp.read())
    #        fp.close()
    #        img.add_header('Content-ID', '<'+attachment+'>')
    #        img.add_header('Content-Disposition', 'inline',filename=attachment)
    #        msg.attach(img)
    data=msg.as_string()
    dataout=data.encode('utf8')
    atpic.log.debug(yy,'output=',dataout)
    return dataout


def sendmail_postfix(mail_recipients,data):
    """
    recipients: a list of email address
    data: a MIME message
    """
    yy=atpic.log.setname(xx,'sendmail_google')
    atpic.log.debug(yy,'input=',(mail_recipients,data))

    # gmail_user="atpicversion2@gmail.com"
    # gmail_pwd="atpic4tux"
    mail_from="no-reply@atpic.com"
    sentok=True
    mail_recipients_string=[]
    for mail_rec in mail_recipients:
        mail_recipients_string.append(mail_rec.decode('utf8'))
    try:
        smtpserver = smtplib.SMTP("localhost", 25)
        smtpserver.set_debuglevel(0) # set to 1 if want to stdout
        smtpserver.sendmail(mail_from, mail_recipients_string, data.decode('utf8'))
        atpic.log.debug(yy,'done!')
        smtpserver.close()
    except:
        atpic.log.error(yy,traceback.format_exc())
        sentok=False
    atpic.log.debug(yy,'output=sentok=',sentok)
    return sentok

def sendmail_google(mail_recipients,data):
    """
    recipients: a list of email address
    data: a MIME message
    """
    yy=atpic.log.setname(xx,'sendmail_google')
    atpic.log.debug(yy,'input=',(mail_recipients,data))

    gmail_user="atpicversion2@gmail.com"
    gmail_pwd="atpic4tux"
    sentok=True
    mail_recipients_string=[]
    for mail_rec in mail_recipients:
        mail_recipients_string.append(mail_rec.decode('utf8'))
    try:
        try:
            # ssl context cannot be set in uwsgi, only at top level globalcon
            # so first check if a global ssl context has been defined
            sslcontext=atpic.globalcon.mysslcontext
        except:
            sslcontext=None
        smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465,context=sslcontext)
        smtpserver.set_debuglevel(0) # set to 1 if want to stdout
        smtpserver.login(gmail_user,gmail_pwd)
        smtpserver.sendmail(gmail_user, mail_recipients_string, data.decode('utf8'))
        atpic.log.debug(yy,'done!')
        smtpserver.close()
    except:
        atpic.log.error(yy,traceback.format_exc())
        sentok=False
    atpic.log.debug(yy,'output=sentok=',sentok)
    return sentok

def sendmail(mail_recipients,data):
    """
    recipients: a list of email address
    data: a MIME message
    """
    yy=atpic.log.setname(xx,'sendmail')
    atpic.log.debug(yy,'input=',(mail_recipients,data))
    islocal=atpic.whatismyip.get_islocal()
    if islocal:
        sentok=sendmail_google(mail_recipients,data)
    else:
        sentok=sendmail_postfix(mail_recipients,data)
    return sentok

def postprocessing(dataerror,hxplo,pxplo,actions,indata,environ,xmlo):
    """
    Decides if we need to send a mail
    """
    yy=atpic.log.setname(xx,'postprocessing')
    atpic.log.debug(yy,'input=',(dataerror,hxplo.list(),pxplo.list(),actions,indata,environ,xmlo.data.content))

    if pxplo.keys()==[b'forgot'] and actions==[b'post']:
        atpic.log.debug(yy,'this is a post to forgot')
        xml_string=xmlo.data.content
        xml_doc = etree.parse(io.BytesIO(b''.join(xml_string)))
        atpic.log.debug(yy,'extracting email address')
        userhash={}
        for elname in ['id','email','servershort','name']:
            for elem in xml_doc.xpath('//'+elname):
                # atpic.log.debug(yy,'elem',elem,dir(elem))
                userhash[elname]=elem.text.encode('utf8')
                atpic.log.debug(yy,'elname',elname,userhash[elname])
                elem.getparent().remove(elem) # we need to hide what we postponed to hide (see worker.py forgot)
        if dataerror=={}:
            atpic.log.debug(yy,'no error we need to send a mail to',userhash)
            # will need a tmpsession
            # authenticatecrypto.make_session(b'tmpses',b'atpic.com',t3b,b'1',b'alexmadon',b'Alex M')
        
            t3b=atpic.authenticatecrypto.set_endoflife(3*60) # 3 minutes
            host=environ.get(b'HTTP_HOST',b'atpic.com')
            servicename=b'atpic.com'
            session=atpic.authenticatecrypto.make_session(b'session',servicename,t3b,userhash['id'],userhash['servershort'],userhash['name'])
            atpic.log.debug(yy,'session',session)
            reseturl=b'http://'+host+b'/reset/'+session
            atpic.log.info(yy,'reseturl',reseturl)

            # then forge a mail to (see forgot.py)
            # GET http://atpic.com/reset/xyzzzzzzzz (presents a from to reset passwd if session is valid, reminds the login)
            mail_recipients=[userhash['email'],]
            
            mail_subject=b"resetting your atpic.com password"
            mail_html=b'''
<html>
<body>
<h1>To reset your atpic.com password</h1>
click on the link below:<br/>
<a href="'''+reseturl+b'''">'''+reseturl+b'''</a>
</body>
</html>
'''

            data=create_data(mail_subject,mail_html)
            sentok=sendmail(mail_recipients,data)
            if sentok:
                sentokstring=b'sentok'
            else:
                sentokstring=b'sentfailed'
            atpic.log.debug(yy,'sentokstring=',sentokstring)
        else:
            atpic.log.debug(yy,'there was an error: NO MAIL to send')
            sentokstring=b'sentfailed'


        for elem in xml_doc.xpath('//forgot'):
            # atpic.log.debug(yy,'elem',elem,dir(elem))
            elem.append(etree.Element(sentokstring))
        xml_string=etree.tostring(xml_doc)
        xmlo.data.content=[xml_string,]

    atpic.log.debug(yy,'output=',xmlo.data.content)
    return xmlo

if __name__ == "__main__":
    print('sending mail')
    # mail_recipients=[b"alex.madon@gmail.com",]
    mail_recipients=[b"alex@madon.net",]

    mail_subject=b"test 5"
    mail_html=b"""
<html>
<body>
<h1>this is a test</h1>
</body>
</html>
"""

    data=create_data(mail_subject,mail_html)
    sentok=sendmail(mail_recipients,data)
    print('sentok',sentok)
