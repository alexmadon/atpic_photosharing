#!/usr/bin/python3

import re
import traceback
import os
import os.path
import time

import atpic.libpqalex
import atpic.magic3k
import atpic.log
from atpic.mybytes import *
import atpic.hashat
import atpic.pathstore
import atpic.xmlutils
import atpic.zmq_asyncpro_client

xx=atpic.log.setmod("INFO","processinfiles")

def mime2extension(amime):
    """
    Converts a mime type to a 3 letter extension
    """
    # could use the mimetrypes modules
    # but not well adapted as most photo raw formats are unkown
    # can be unit tested    
    complic={
        b'image/jpeg':b'jpg',
        b'video/quicktime':b'mov',
        b'video/3gpp2':b'3g2',
        b'video/3gpp':b'3gp',
        b'video/mpeg':b'mpg',
        }
    if amime in complic.keys():
        extension=complic[amime]
    else:
        extension=amime[-3:]
    return extension


def get_goodfilename(pid,extension,infilename):
    # this goodfilename should statisfy the name constraints 
    # and take into account the slug passed in the header
    #  and default to PID.extension
    yy=atpic.log.setname(xx,'get_goodfilename')
    goodfilename=b''
    atpic.log.debug(yy,pid,extension,infilename)
    if infilename==b'' or re.match(b'/',infilename):
        goodfilename=pid+b'.'+extension
    else:
        goodfilename=infilename
    atpic.log.debug(yy,'will return',goodfilename)
    return goodfilename


def process_onefile_synchronous_nosql_getsize(afile):
    yy=atpic.log.setname(xx,'process_onefile_synchronous_nosql_getsize')
    # then we need to extract size info
    # this is done synchronously as we need the ctime in fuse? NOT anymore: in fuse we do a stat on the file in real time
    atpic.log.debug(yy,'input=',afile)
    file_stat=os.stat(afile)
    st_size=file_stat.st_size # size in bytes
    st_size=int2bytes(st_size) # convert to b''
    atpic.log.debug(yy,'st_size',st_size)
    return st_size

def process_onefile_synchronous_nosql_getmagic(afile):
    # do really quick MIME type guess
    yy=atpic.log.setname(xx,'process_onefile_synchronous_nosql_getmagic')
    magic_mime=atpic.magic3k.mymime_from_file(afile)
    atpic.log.debug(yy,'magic_mime',magic_mime)
    # convert mime to extension
    extension=mime2extension(magic_mime)
    [mimetype_magic,mimesubtype_magic]=magic_mime.split(b'/')
    atpic.log.debug(yy,"mimetype_magic",mimetype_magic,"mimesubtype_magic",mimesubtype_magic)
    return (extension,mimetype_magic,mimesubtype_magic)


def process_onefile_synchronous_nosql_move2pathstore(afile,pathstore,partition):
    yy=atpic.log.setname(xx,'process_onefile_synchronous_nosql_move2pathstore')
    atpic.log.debug(yy,'input=',(afile,pathstore,partition))
    (dirpath,filename)=os.path.split(pathstore)
    # side effect: remake the directory:
    fulldirpath=b'/'+partition+b'/'+dirpath
    atpic.log.debug(yy,"fulldirpath=",fulldirpath)
    os.makedirs(fulldirpath,exist_ok=True)
    # move or copy?
    destination=fulldirpath+b"/"+filename
    atpic.log.debug(yy,"destination",destination)
    os.rename(afile,destination) # this is the move or mv

def process_onefile_synchronous_nosql(afile,original_name,partition,uid,pid):
    """
    This has not SQL dependency to make unit testing easier
    """
    yy=atpic.log.setname(xx,'process_onefile_synchronous_nosql')
    # ################################################# 
    #  SYNCHRONOUS
    # ################################################# 
    # first we need a fast (synchronous) evaluation of mime type 
    # (needed for the extension and store file name)
    # we use libmagic python3 ctypes wrapper
    
    # first we work on the tmp file:
    # getting the size
    st_size=process_onefile_synchronous_nosql_getsize(afile)
    # and the magic
    (extension,mimetype_magic,mimesubtype_magic)=process_onefile_synchronous_nosql_getmagic(afile)
    
    # then we need to move the tmp file to the correct folder 
    # in time and user
    # this is done synchronously
    resolution=b"0"
    pathstore=atpic.pathstore.forge_pathstore(uid,pid,resolution,extension)
    
    # move the tmpfile to pathstore
    process_onefile_synchronous_nosql_move2pathstore(afile,pathstore,partition)

    goodfilename=get_goodfilename(pid,extension,original_name)
    return (st_size,extension,mimetype_magic,mimesubtype_magic,pathstore,goodfilename)


def process_onefile_synchronous_sql(afile,partition,uid,gid,pid,st_size,extension,mimetype_magic,mimesubtype_magic,pathstore,goodfilename,db):

    yy=atpic.log.setname(xx,'process_onefile_synchronous_sql')

    query=b"UPDATE _user_gallery_pic SET _sizeb=$1, _extension=$2, _mimetype_magic=$3, _mimesubtype_magic=$4, _originalname=$5,_pathstore=$6 WHERE _user=$7 AND _gallery=$8 AND id=$9 RETURNING *"
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',(st_size,extension,mimetype_magic,mimesubtype_magic,goodfilename,pathstore,uid,gid,pid,))
    result=atpic.libpqalex.process_result(result)
    
    atpic.log.debug(yy,"result",result)

    # then we update the _usage column of _user
    query=b"UPDATE _user SET _usage = _usage + $1 WHERE id=$2 RETURNING *" # _usage implements quotas
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',(st_size,uid,))
    result=atpic.libpqalex.process_result(result)
    
    atpic.log.debug(yy,"result",result)
    return result

def process_onefile_fuse(afile,apath,db):
    # in fuse we have only two path: the tmp path and the requested path
    # no uid, no gid, no pid (yet if creation)
    # we have either  to update or to create a row in the _user_gallery_pic
 
    # at this stage we should have the uid, gid, pid (and partition?)

    pass

def process_onefile(afile,original_name,partition,uid,gid,pid,db):
    yy=atpic.log.setname(xx,'process_onefile')

    # ################################################# 
    #  SYNCHRONOUS
    # ################################################# 
    atpic.log.info(yy,'input=',(afile,original_name,partition,uid,gid,pid,db))
    # synchronous no sql
    atpic.log.info(yy,'doing synchronous work')
    atpic.log.debug(yy,'start synchronous no sql')
    (st_size,extension,mimetype_magic,mimesubtype_magic,pathstore,goodfilename)=process_onefile_synchronous_nosql(afile,original_name,partition,uid,pid)
    atpic.log.debug(yy,'end synchronous no sql')

    # synchronous sql
    atpic.log.debug(yy,'start synchronous sql')
    result=process_onefile_synchronous_sql(afile,partition,uid,gid,pid,st_size,extension,mimetype_magic,mimesubtype_magic,pathstore,goodfilename,db)
    atpic.log.debug(yy,'end synchronous sql')

    
    # ################################################# 
    #  ASYNCHRONOUS
    # #################################################
    # all asyncrhonous processing is sent to a zeromq queue that sends to a VM
    # message=b'T|123456|1|9999|var/www/jpg|tropic.jpg'
    atpic.log.info(yy,'need some asynchronous work')
    timestamp=float2bytes(time.time())
    message=b'|'.join((b'T',timestamp,uid,pid,partition,pathstore))
    atpic.log.info(yy,'asynchronous message to send:',message)

    atpic.zmq_asyncpro_client.send(message)


    return (st_size,extension,mimetype_magic,mimesubtype_magic,pathstore,goodfilename)




def update_xmlo(xml_string,st_size,extension,mimetype_magic,mimesubtype_magic,pathstore,goodfilename,partition,pid):
    # we update the XML sql response with the new fields we created (mime magic, etc..)
    yy=atpic.log.setname(xx,'update_xmlo')
    atpic.log.debug(yy,'input=',xml_string,st_size,extension,mimetype_magic,mimesubtype_magic,pathstore,goodfilename)
    basepath=b'/USER/GALLERY/pic'

    resolutioncode=b'0'
    hashvalue=atpic.hashat.forge_pathstorehash(pid,resolutioncode,pathstore,partition,extension)


    anarray={b'size0':st_size,b'extension':extension,b'mimetype_magic':mimetype_magic,b'mimesubtype_magic':mimesubtype_magic,b'pathstore':hashvalue,b'originalname':goodfilename}
    xml_string=atpic.xmlutils.replace_params(xml_string,basepath,anarray)
    return xml_string

def process_infiles(xmlo,actions,indata,db):
    """
    Used to store the first upload of the file
    infiles a list of files (list length should be 1)
    xmlo is used to get user and gallery and pic (id) parameters

    Note: this function has many side effects, 
    so unit testing is more on the components
    """
    yy=atpic.log.setname(xx,'process_infiles')
    if actions[0]==b"get":
        return xmlo
    try:
        atpic.log.debug(yy,"indata=",indata)    
        xml_string=b''.join(xmlo.data.content)
        atpic.log.debug(yy,xml_string)   
        # we need to extract for the XML the image parameters
        # like pid, gid, uid, device, etc... 
        (partition,uid,gid,pid)=atpic.xmlutils.get_new_image_params(xml_string)
        atpic.log.debug(yy,"params", partition, uid, gid, pid)   
        for (key,isfile,value) in indata:
            if isfile:
                (afile,original_name,original_mime)=value
                (st_size,extension,mimetype_magic,mimesubtype_magic,pathstore,goodfilename)=process_onefile(afile,original_name,partition, uid, gid, pid, db)
                xml_string=update_xmlo(xml_string,st_size,extension,mimetype_magic,mimesubtype_magic,pathstore,goodfilename,partition,pid)
                # update the XML with what we have found
                xmlo.data.content=[xml_string,]
                xmlo.data.stack=[]
        return xmlo
        
    except atpic.xmlutils.XMLnotValid:
        # need some cleansing
        # some logging:
        atpic.log.error(yy,'XMLnotValid')
        atpic.log.error(yy,traceback.format_exc())

        return xmlo

        # and the pass
    except IndexError:
        atpic.log.error(yy,'IndexError')
        atpic.log.error(yy,traceback.format_exc())
        return xmlo


"""
You have:
1) a tmpfile on disk (both fuse and web upload)
2) something that identifies the user/gallery/picture
 a) in fuse: a requested path
 b) in SQL: a XML file

You need:
- partition

You SQL:
insert/update pathstore, extension, size_t, original file name cleaned, date

You will return:
1) a pathstore
2) an extension

-----------------------
later for artefacts:

"""

if __name__ == "__main__":
    pass
