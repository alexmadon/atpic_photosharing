#!/usr/bin/python3
# this should run in a virtual machine
# there is a protocol
# input -> output (that can be used to update SQL)
# make it simple first, we'll see performance optimisations later
# (e.g exiftool)


# there is a protocol as input (can test)
# there is a protocol as output (as is input of SQL)

"""

There is a dispatcher:
extract mimetype,width,height with exiftool
if video-> extract frames
elif image/raw->convert to jpg with dcraw
elif image -> if width,height ->thumbnail with convert
"""

import time
import os
import os.path

import atpic.convert_image
import atpic.pathstore
import atpic.dcraw
import atpic.exiftool3k
import atpic.exiftool_parse
import atpic.mybytes
import atpic.log
import atpic.videothumb
import atpic.imageborders
import atpic.zmq_asyncdone_client


xx=atpic.log.setmod("INFO","asyncpro")

def callback_dummy(x,msg):
    pass

def callback_log(x,msg):
    yy=atpic.log.setname(xx,'callback_log')
    atpic.log.info(yy,'LOGGING',msg)


def supported_raw():
    alist=[
        # b'image/jpeg'
        b'image/x-canon-crw',
        b'image/x-canon-cr2',
        b'image/x-fujifilm-raf',
        b'image/x-minolta-mrw',
        b'image/x-nikon-nef',
        b'image/x-olympus-orf',
        b'image/x-pentax-pef',
        b'image/x-sigma-x3f',
        b'image/x-sony-arw',
        ]
    return alist


def supported_video():
    alist=[
        b'video/x-msvideo',
        b'video/mpeg',
        b'video/3gpp',
        b'video/3gpp2',
        b'video/x-m4v',
        b'video/quicktime',
        b'video/mpeg',
        b'video/mp4',
        b'video/quicktime',
        ]
    return alist








def get_resolution_todo(amax):
    # as input a size (max of width and height)
    # returns the list of resolutions to create
    amb=atpic.mybytes.bytes2int(amax)
    if amb> 1200:
        res=[b'1024',b'600',b'350',b'160',b'70']
    elif amb> 720:
        res=[b'600',b'350',b'160',b'70']
    elif amb> 420:
        res=[b'350',b'160',b'70']
    elif amb> 190:
        res=[b'160',b'70']
    elif amb> 90:
        res=[b'70']
    else:
        res=[]
    return res



def set_extension_reduce(mime_type):
    if mime_type==b'image/gif':
        extension=b'gif'
    elif mime_type==b'image/png':
        extension=b'png'
    else:
        extension=b'jpg'
    return extension









def process_imagemagick(fullpath,output,uid,pid,partition,extension,amax,callback,socketres):
    yy=atpic.log.setname(xx,'process_imagemagick')
    for asize in get_resolution_todo(amax):
        atpic.log.debug(yy,'doing resolution',asize)

        code=b'r'+asize
        infile=fullpath
        processfct=getattr(atpic.convert_image,'convert_convert_'+asize.decode('utf8'))
        (output,outfile)=process_basic(processfct,output,infile,uid,pid,partition,code,extension,callback,socketres)
    return output

def process_video(fullpath,output,uid,pid,partition,extension,aheight,amax,callback,socketres):
    # 
    yy=atpic.log.setname(xx,'process_video')
    atpic.log.debug(yy,'input=',(fullpath,output,uid,pid,partition,extension,aheight,amax,callback,socketres))

    # first extract a raw:
    processfct=getattr(atpic.videothumb,'totemvideothumbnailer')
    extension=b'png'
    code=b'v0'
    infile=fullpath
    (output,outfile1)=process_basic(processfct,output,infile,uid,pid,partition,code,extension,callback,socketres)

    # put borders on that raw:
    processfct=getattr(atpic.imageborders,'put_borders')
    extension=b'png'
    code=b'vf0' # video framed by perforations
    infile=outfile1
    (output,outfile2)=process_basic(processfct,output,infile,uid,pid,partition,code,extension,callback,socketres,other_args=[aheight])


    # now all the smaller pictures
    for asize in get_resolution_todo(amax):
        atpic.log.debug(yy,'doing resolution',asize)

        code=b'v'+asize
        infile=outfile1
        processfct=getattr(atpic.convert_image,'convert_convert_'+asize.decode('utf8'))
        (output,outfile)=process_basic(processfct,output,infile,uid,pid,partition,code,extension,callback,socketres)

        # with frame
        code=b'vf'+asize
        infile=outfile2
        processfct=getattr(atpic.convert_image,'convert_convert_'+asize.decode('utf8'))
        (output,outfile)=process_basic(processfct,output,infile,uid,pid,partition,code,extension,callback,socketres)

    return output


def process_basic(processfct,output,infile,uid,pid,partition,code,extension,callback,socketres,other_args=[]):
    # will call processfct(infile,outfile)
    # and send a message
    # returns (output,outfile)
    # outfile is built with (uid,pid,code,extension)
    yy=atpic.log.setname(xx,'process_basic')
    atpic.log.debug(yy,'input=',(processfct,output,infile,uid,pid,partition,code,extension,callback,socketres))

    pathstore=atpic.pathstore.forge_pathstore(uid,pid,code,extension)
    outfile=b'/'+partition+b'/'+pathstore
    atpic.log.debug(yy,'outfile will be:',outfile)
    thedir=os.path.dirname(outfile)
    os.makedirs(thedir,exist_ok=True)
    
    # do the processing
    if other_args==[]:
        processfct(infile,outfile)
    else:
        processfct(infile,outfile,other_args)

    # get the size of the outfile
    astats=os.stat(outfile)
    atpic.log.debug(yy,'stats for file',outfile,astats)
    sizeb=astats.st_size
    
    # message [A=artefact,uid,pid,sizeb,code,extension,pathstore]
    send_msg=[b'A',uid,pid,atpic.mybytes.int2bytes(sizeb),code,extension,pathstore] # artefact
    send_msg_concat=b'|'.join(send_msg)
    output.append(send_msg_concat)

    callback(socketres,send_msg_concat)
    # return the message and the name of the resulting file
    atpic.log.debug(yy,"output=",(output,outfile))
    return (output,outfile)

def process(message,socketres):
    # socektres is used for the normal callback (to done server)
    # PROTOCOL:
    # (action,timestamp,uid,pid,partition,path)
    # input message is T|timestamp|UID|PID|partition|path (T=Transform)
    # action defines what callback to use:
    # T=normal transform with callback
    # D=dummy
    # L=Log
    # this is a sequence of side effect (transformations)
    # could do one call back for easier testing
    # or one after each action
    # once the mime type is known, we should know the list of transformations
    # This function has many side effects
    # it typically sends back to a listener a message that inserts data into SQL
    # in testing mode, we use the output that is not used in production mode
    # ouput is a list of the messages that are sent to SQL

    yy=atpic.log.setname(xx,'process')
    atpic.log.debug(yy,"input=",message)
    output=[] # used only in testing mode to compare with what is expected

    time1=time.time()
    (action,timestamp,uid,pid,partition,path)=message.split(b'|')
    atpic.log.debug(yy,"splitted",(action,timestamp,uid,pid,partition,path))

    # set the callback depending on 'action'
    if action==b'T': # Transform
        callback=atpic.zmq_asyncdone_client.send # used in production
    elif action==b'D': # Debug
        callback=callback_dummy # used for unit testing
    elif action==b'L': # Log
        callback=callback_log # used to check life




    # first extract xml exif data
    fullpath=b'/'+partition+b'/'+path


    # =============================
    # save the xml exif data to disk
    # ==============================    
    extension=b'xml'
    code=b'exif'
    infile=fullpath
    processfct=atpic.exiftool3k.process
    (output,outfile)=process_basic(processfct,output,infile,uid,pid,partition,code,extension,callback,socketres)


    # ================================
    # extract important data from exif:
    # ================================
    f=open(outfile,'rb')
    thexml=f.read()
    f.close()
    important=atpic.exiftool_parse.parse(thexml)
    atpic.log.debug(yy,'important=',important)
    # send a message to update SQL metadata
    send_msg=[b'U',uid,pid]+list(important) # SECURITY: need to clean
    output.append(b'|'.join(send_msg)) # update


    # depending on mime type, do video or pic thumbnailing
    mime_type=important[0]
    awidth=important[1]
    aheight=important[2]
    amax=max(awidth,aheight)
    atpic.log.debug(yy,'mime_type=',mime_type)

    """
    _code 
    -------
 r1024
 r350
 r160
 r70
 r600

artefact:

_code      | r1024
_datestore | 2013-10-19 12:51:36.395893
_extension | jpg
_pathstore | o/2567/26683/0/1181456/1024.jpg
_pic       | 1181456
_sizeb     | 0
_user      | 2567
id         | 330966



    $resolutions[]="1024";
    $resolutions[]="600";
    $resolutions[]="350";
    $resolutions[]="160";
    $resolutions[]="70";
    //if image is smaller that 160, we should not make the thumb
        if ($maxwidth_length>plus_margin_percent(160)){

"""
    if mime_type.startswith(b'image'):
        # is that a RAW format?
        if mime_type in [b'image/jpeg',b'image/png',b'image/gif',]:
            atpic.log.debug(yy,'this is a jpg or similar (non raw)')
            extension=set_extension_reduce(mime_type)
            output=process_imagemagick(fullpath,output,uid,pid,partition,extension,amax,callback,socketres)

        elif mime_type in supported_raw():
            atpic.log.debug(yy,'this is a raw')
            # do dcraw

            extension=b'jpg'
            code=b'0'
            infile=fullpath
            processfct=atpic.dcraw.ufraw_convert # DCRAW
            (output,outfile)=process_basic(processfct,output,infile,uid,pid,partition,code,extension,callback,socketres)


            # then generate all the JPGs, use as input the ouput of dcraw
            output=process_imagemagick(outfile,output,uid,pid,partition,extension,amax,callback,socketres)


    elif mime_type.startswith(b'video'):
        atpic.log.debug(yy,'this is a video')
        output=process_video(fullpath,output,uid,pid,partition,extension,aheight,amax,callback,socketres)

        pass
    else:
        atpic.log.warn(yy,'unsupported mimetype!!!',mime_type)

    # with artefact id (to be compared in testing mode)

    # finally put the original message:
    output.append(message)
    callback(socketres,message)

    time2=time.time()
    ittook=time2-time1
    atpic.log.debug(yy,"It took (seconds):",ittook)
    return output





if __name__ == "__main__":
    yy=atpic.log.setname(xx,'main')
    print('hi')
    def callback_dummy(x):
        pass
    message=b'T|1|9999|home/madon/jpg|866475.jpg'
    output=process(message,callback_dummy,None)
    for line in output:
        print(line)
