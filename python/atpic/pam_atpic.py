#
# this code is called using exec() in python 2.7 
# (see how to check version below)
# we use python2.7 zmq as light connector to more complex software in python3
#!/usr/bin/python3
# or /usr/bin/python2.7 ????
import syslog
import sys
import zmq

import traceback


# http://howto.gumph.org/content/setup-virtual-users-and-directories-in-vsftpd/


# http://ace-host.stuart.id.au/russell/files/pam_python/doc/index.html

# http://www.chokepoint.net/2014/01/more-fun-with-pam-python-failed.html

def check_authenticated(user,password):
    context = zmq.Context()    
    # Socket to talk to server
    syslog.syslog("Connecting to authentication server...")
    socket = context.socket(zmq.REQ)
    socket.connect ("tcp://localhost:5558")
    request=user+":"+password # should we crypt? or use a unix socket
    # difficult to crypt, because we have a hash stored in db
    socket.send (request)
    # Get the reply.
    message = socket.recv()
    syslog.syslog("response is %s" % message)
    socket.close()
    if message=='ok':
        output=True
    else:
        output=False
        # syslog.syslog("FTP Auth Failed: (%s:%s)" % (user, password))

    syslog.syslog("will return %s" % output)
    return output

def pam_sm_authenticate(pamh, flags, argv):
    syslog.syslog("start pam_sm_authenticate")
    syslog.syslog("my python version is: "+sys.version)
    syslog.syslog("pamh %s" % pamh)
    # get username
    try:
        syslog.syslog("try to get user")
        user = pamh.get_user(None)
    except pamh.exception, e:
        syslog.syslog("failed to get user")
        return e.pam_result
    if user == None:
        syslog.syslog("setting to nobody")
        pam.user = "nobody"

    # get password
    # in openpam, could be already in pamh.authtok
    try:
        resp = pamh.conversation(pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, 'Password:'))

        password=resp.resp
        # syslog.syslog("Remote Host: %s (%s:%s)" % (pamh.rhost, user, password))
        syslog.syslog("Remote Host: %s (%s:XXXX)" % (pamh.rhost, user))
    except pamh.exception, e:
        return e.pam_result
    try:
        authenticated=check_authenticated(user,password)
    except:
        syslog.syslog(traceback.format_exc())

    if authenticated:
        syslog.syslog('user authenticated OK')
        return pamh.PAM_SUCCESS
    else:
        return pamh.PAM_AUTH_ERR

    # return pamh.PAM_SUCCESS
    # try:
    #     syslog.syslog("got password: "+pamh.authtok)
    #     return pamh.PAM_SUCCESS
    # except:
    #     syslog.syslog("exception!")
    #     return pamh.PAM_AUTH_ERR

def pam_sm_setcred(pamh, flags, argv):
    syslog.syslog("pam_sm_setcred")
    return pamh.PAM_SUCCESS


def pam_sm_acct_mgmt(pamh, flags, argv):
    syslog.syslog("pam_sm_acct_mgmt")
    return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
    syslog.syslog("pam_sm_open_session")
    return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
    syslog.syslog("pam_sm_close_session")
    return pamh.PAM_SUCCESS

def pam_sm_chauthtok(pamh, flags, argv):
    syslog.syslog("pam_sm_chauthtok")
    return pamh.PAM_SUCCESS



if __name__ == "__main__":
    print ('hi')
    user="toto"
    password="mypass"
    res=check_authenticated(user,password)
    print('res=',res)
