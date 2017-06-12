#!/usr/bin/python3
import atpic.log
xx=atpic.log.setmod("INFO","indatautils")


def get(indata,key,default):
    """
    Gets the first key
    """
    # captchapublic=indata[0][b'captchapublic'][0]
    # captchahidden=indata[0][b'captchahidden'][0]
    yy=atpic.log.setname(xx,'get')
    atpic.log.debug(yy,'input=',(key,indata,default))
    out=default
    for (akey,aisfile,avalue) in indata:
        if akey==key:
            out=avalue
            break
    atpic.log.debug(yy,'output=',out)
    return out

def setdic(indata):
    """
    Transforms the indata list into a dictionary.
    The values of the dictionnary are not list but bytes
    """
    yy=atpic.log.setname(xx,'setdic')
    atpic.log.debug(yy,'input=',indata)
    adic={}
    for (akey,aisfile,avalue) in indata:
        if not aisfile:
            adic[akey]=avalue
    atpic.log.debug(yy,'output=',adic)
    return adic

def setdicfiles(indata):
    """
    Transforms the indata list into a dictionary.
    The values of the dictionnary are not list but bytes
    If there is a file, then create a original name entry.
    """
    yy=atpic.log.setname(xx,'setdicfiles')
    atpic.log.debug(yy,'input=',indata)
    adic={}
    for (akey,aisfile,avalue) in indata:
        if aisfile:
            adic[b'originalname']=avalue[1]
        else:
            adic[akey]=avalue
    atpic.log.debug(yy,'output=',adic)

    return adic



def update(indata,key,newvalue):
    yy=atpic.log.setname(xx,'update')
    atpic.log.debug(yy,'input=',(indata,key,newvalue))
    newindata=[]
    for (akey,aisfile,avalue) in indata:
        if aisfile:
            newindata.append((akey,aisfile,avalue))
        else:
            if akey==key:
                newindata.append((akey,aisfile,newvalue))
            else:
                newindata.append((akey,aisfile,avalue))

    atpic.log.debug(yy,'output=',newindata)
    return newindata

def upsert(indata,key,newvalue):
    yy=atpic.log.setname(xx,'upsert')
    atpic.log.debug(yy,'input=',(indata,key,newvalue))
    newindata=[]
    found=False
    for (akey,aisfile,avalue) in indata:
        if aisfile:
            newindata.append((akey,aisfile,avalue))
        else:
            if akey==key:
                found=True
                newindata.append((akey,aisfile,newvalue))
            else:
                newindata.append((akey,aisfile,avalue))
    if not found:
        newindata.append((key,False,newvalue))
    atpic.log.debug(yy,'output=',newindata)
    return newindata

def insert_ifnull(indata,key,newvalue):
    yy=atpic.log.setname(xx,'insert_ifnull')
    atpic.log.debug(yy,'input=',(indata,key,newvalue))
    newindata=[]
    found=False
    for (akey,aisfile,avalue) in indata:
        if aisfile:
            newindata.append((akey,aisfile,avalue))
        else:
            if akey==key:
                found=True
            newindata.append((akey,aisfile,avalue))
    if not found:
        newindata.append((key,False,newvalue))
    atpic.log.debug(yy,'output=',newindata)
    return newindata


def keys(indata):
    yy=atpic.log.setname(xx,'keys')
    atpic.log.debug(yy,'input=',indata)
    keys=[]
    for (akey,aisfile,avalue) in indata:
        if not aisfile:
            keys.append(akey)
    atpic.log.debug(yy,'output=',keys)
    return keys
