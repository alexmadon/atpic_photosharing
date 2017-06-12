#!/usr/bin/python3
"""
Authenticates at login with a user/password.
This is different from the session based authentication.
Once a session is created no SQL query is necessary
But to create a session, we need a SQL lookup with username and password.
"""
# import logging
import atpic.log

import atpic.authenticatecrypto
import atpic.libpqalex


xx=atpic.log.setmod("INFO","authenticatesql")




def check_username_password(username,password,db):
    """
    Returns True is the password matches the encrypted password in DB.
    """
    yy=atpic.log.setname(xx,'check_username_password')
    atpic.log.debug(yy,username,password,db,sep=',')
    # lookup the SQL row based on username
    query=b"select * from _user where _login=$1"
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',(username,))
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,'db result', result)
    # if no user found or more than one user found returns a failure
    reslen=len(result)
    atpic.log.debug(yy,"reslen",reslen)
    if reslen != 1:
        return (False,())
    else:
        # if exactly one row is found, get the encrypted password
        encpassword=result[0][b"_password"]
        userid=result[0][b"id"]
        servershort=result[0][b"_servershort"]
        name=result[0][b"_name"]
        atpic.log.debug(yy,"encpassword %s" % encpassword)
        # check that the encrypted password from sql is the same 
        # as the encryption of the HTTP posted 
        salt=encpassword[0:2]
        atpic.log.debug(yy,"salt",salt)
        encpassword_posted=atpic.authenticatecrypto.mycrypt(password,salt)
        atpic.log.debug(yy,"encpassword_posted",encpassword_posted)
        if encpassword==encpassword_posted:
            return (True,(userid,servershort,name))
        else:
            return (False,())
    return (False,())


if __name__ == "__main__":


    username=b"someuser"
    password=b"somepasswd"
    db=atpic.libpqalex.db()

    (success,userid)=check_username_password(username,password,db)
    print("success",success,userid)
