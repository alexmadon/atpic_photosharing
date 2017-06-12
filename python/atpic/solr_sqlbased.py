#!/usr/bin/python3
# avoid tmp tables
# no cascade of gallery tags to pictures
# but return the tagged gallery (should work OK as licence is per gallery)
# drawback: could get duplicates (individual pic + parent gallery)

# geolocation is not cascaded to children: return the gallery and/or the pic

# licence: only slow operation is update of licence (+price?)
# this is the equivalent of a chmod -R

# driver:
# xml for solr
# json for elacticsearch
# 

import io
import datetime
import random
import sys

import atpic.log
import atpic.redis_pie
from atpic.redisconst import *
import atpic.mybytes
import atpic.tokenizer

import atpic.libpqalex

xx=atpic.log.setmod("INFO","solr_sqlbased")


# ##############################
# driver definition
# ##############################
def get_driver():
    return b'json'

def espacedoublequotes(fieldvalue):
    return fieldvalue.replace(b'"',b'\\"')

def myappend(outlist,fieldname,fieldvalue):
    # may need a number=true extra parameter (in json does not need double quotes)
    if get_driver()==b'xml':
        outlist.append(b'<field name="'+fieldname+b'">'+fieldvalue+b'</field>')
    else:
        # json:
        fieldvalue=espacedoublequotes(fieldvalue)




        outlist.append(b'"'+fieldname+b'" : "'+fieldvalue+b'"')
    return outlist

def myjoin(outlist):
    if get_driver()==b'xml':
        return b''.join(outlist)
    else:
        return b', '.join(outlist)



def mylatlon(lat,lon,outlist):
    if get_driver()==b'xml':
        myappend(outlist,b'latlon_0_coordinate',lat) # 
        myappend(outlist,b'latlon_1_coordinate',lon) # 
    else:
        outlist.append(b'"location" : { "lat" : '+lat+b', "lon" : '+lon+b'}') 
    return outlist

# ##############################
# user elementary functions
# ##############################

def get_user(id):
    yy=atpic.log.setname(xx,'get_user')
    atpic.log.debug(yy,'input=',id)
    query=b"select _user.*,storing.fasturl_atpic,storing.serverip from _user join storing on storing.id=_user._storefrom where _user.id=$1"
    # query=atpic.sqlllib.get_user()
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',(id,))
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,result)
    return result


def xml_user(resuser):
    """
    Display the user resuser in XML
    """
    yy=atpic.log.setname(xx,'xml_user')
    

    atpic.log.debug(yy,resuser)
    atpic.log.debug(yy,dir(resuser))
    atpic.log.debug(yy,resuser.keys())
    outlist=[]
    myappend(outlist,b'user',resuser[b'id']) # user ID
    myappend(outlist,b'username',resuser[b'_name']) # user name
    # myappend(outlist,b'storeurl',resuser[b'fasturl_atpic'])
    # myappend(outlist,b'storefrom',resuser[b'_storefrom'])
    # myappend(outlist,b'serverip',resuser[b'serverip'])
    myappend(outlist,b'servershort',resuser[b'_servershort'])
 
    
    return outlist


# ##############################
# gallery elementary functions
# ##############################
def get_user_gallery(id,uid):
    yy=atpic.log.setname(xx,'get_user_gallery')
    atpic.log.debug(yy,'input=',id)
    query=b"select * from _user_gallery where id=$1 and _user=$2"
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',(id,uid))
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,result)
    return result

def get_gallery_parents_path_recurse(id,uid,path=b'',pathtext=b'',listdir=None,listfile=None,counter=0):
    yy=atpic.log.setname(xx,'get_gallery_parents_path_recurse')
    atpic.log.debug(yy,'input=',id,path,pathtext,listdir,listfile,counter)
    res=get_user_gallery(id,uid)
    # print('XXXXXXX orphan get_gallery_parents_path_recurse',id,uid,res)
    # orphan node: get_gallery_parents_path_recurse b'14241' b'797' []

    res=res[0]
    adir=res[b'_dir']
    if not listdir:
        listdir=[]
    if not listfile:
        listfile=[]
    
    # set path
    path=b'/'+id+path


    # set pathtext        
    if res[b'_file']:
        afile=res[b'_file']
    else:
        afile=id
    pathtext=b'/'+afile+pathtext
    # set listdir 
    listdir.append(id)
    listfile.append(afile)

    counter=counter+1
    if counter< 20 and adir!=b'0': # limit the risk of infinite loops
        (path,pathtext,listdir,listfile,counter)=get_gallery_parents_path_recurse(adir,uid,path,pathtext,listdir,listfile,counter)
    atpic.log.debug(yy,'will return',path,pathtext,listdir,listfile,counter)
    return (path,pathtext,listdir,listfile,counter)

def xml_user_gallery(resuser,resgallery):
    """
    print in XML the gallery part
    """
    yy=atpic.log.setname(xx,'xml_user_gallery')
    outlist=[]

    atpic.log.debug(yy,resgallery.keys())
    myappend(outlist,b'gallery',resgallery[b'id']) # the gallery ID
    # print(b'licence">',resgallery[b'licence'],b'</field>',sep=b'') # 
    myappend(outlist,b'mode',resgallery[b'_mode']) #    
    myappend(outlist,b'dir',resgallery[b'_dir']) # 

    uid=resuser[b'id']
    (path,pathtext,listdir,listfile,counter)=get_gallery_parents_path_recurse(resgallery[b'id'],uid)

    myappend(outlist,b'path',path) # 
    myappend(outlist,b'depth',atpic.mybytes.int2bytes(counter)) # 
    myappend(outlist,b'pathtext',pathtext) # 
    myappend(outlist,b'gtitle',resgallery[b'_title']) # 

    myappend(outlist,b'gtitle_idx',atpic.tokenizer.tokenize(resgallery[b'_title'])) # 
    myappend(outlist,b'gtext_idx',atpic.tokenizer.tokenize(resgallery[b'_text'])) # 


    galleryid=resgallery[b'id']
    uid=resuser[b'id']
    resgallerytag=get_user_gallery_tag(galleryid,uid)
    myappend(outlist,b'gtags',xml_concat(resgallerytag))
    resgalleryphrase=get_user_gallery_phrase(galleryid,uid)
    myappend(outlist,b'gphrase',xml_concat(resgalleryphrase))



    if resgallery[b'_file']:
        afile=resgallery[b'_file']
    else:
        afile=resgallery[b'id']
    myappend(outlist,b'file',afile) # 

    # now the parents (dynamicField)
    depth=0
    listdir.reverse()
    for adir in listdir:
        myappend(outlist,b'dir_'+atpic.mybytes.int2bytes(depth)+b'',adir) # 
        depth=depth+1

    # now the parents (dynamicField)
    depth=0
    listfile.reverse()
    for afile in listfile:
        myappend(outlist,b'file_'+atpic.mybytes.int2bytes(depth)+b'',afile) # 
        depth=depth+1

    return outlist


# ##############################
#  pic  elementary functions
# ##############################

def get_user_gallery_pic(id,uid):
    yy=atpic.log.setname(xx,'get_user_gallery_pic')
    query=b"select * from _user_gallery_pic where id=$1 and _user=$2"
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',(id,uid))
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,result)
    return result


def latlon_valid(lat,lon):
    """
    Solr validates, so we need to make sure it is valid
    """
    yy=atpic.log.setname(xx,'latlon_valid')
    valid=True
    try:
        lat=atpic.mybytes.bytes2float(lat)
        lon=atpic.mybytes.bytes2float(lon)
        if not lat or not lon:
            valid=False
        elif lat<-90 or lat>90 or lon<-180 or lon>180:
            valid=False
    except:
        atpic.log.debug(yy,"XXXXXX latitude longitude invalid",lat,'ZZ',lon,'YY')
        valid=False
    return valid








def get_year(date): # strftime("%Y")
    return date[0:4]

def get_yearmonth(date): # strftime("%Y%m")
    return date[0:4]+date[5:7]

def get_yearmonthday(date): # strftime("%Y%m%d")
    return date[0:4]+date[5:7]+date[8:10]

def get_datexml(datefirst): # strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    """
    Converts SQL time to XML time
    """
    # there is no RFC for XML datetime?
    # rather based on ISO 8601
    # It is expressed in the format [-][Y*]YYYY-MM-DDThh:mm:ss[.s[s*]][TZD].
    # 2002-03-21T19:47:35Z
    parsed=False
    try:
        # try to parse with microseconds
        datetimefirst=datetime.datetime.strptime(datefirst.decode('utf8'),"%Y-%m-%d %H:%M:%S.%f" )
        parsed=True
    except:
        pass
    if not parsed:
        # parse with seconds
        datetimefirst=datetime.datetime.strptime(datefirst.decode('utf8'),"%Y-%m-%d %H:%M:%S" )

    datexml=datetimefirst.strftime("%Y-%m-%dT%H:%M:%S.%fZ").encode('utf8')


    return datexml


def xml_user_gallery_pic(resuser,resgallery,respic):
    """
    print in XML the pic part
    """
    yy=atpic.log.setname(xx,'xml_user_gallery_pic')
    outlist=[]

    atpic.log.debug(yy,respic.keys())
    if respic[b'_datetimeoriginalsql']==b'':
        respic[b'_datetimeoriginalsql']=b'1970-01-01 00:00:00'
    # we need the user ID in the dates!
    # myappend(outlist,b'id',respic[b'id']) # the pic ID
    pid=respic[b'id'] # the pic ID
    myappend(outlist,b'useryear',resuser[b'id']+get_year(respic[b'_datetimeoriginalsql'])) # 
    myappend(outlist,b'useryearmonth',resuser[b'id']+get_yearmonth(respic[b'_datetimeoriginalsql'])) # 
    myappend(outlist,b'useryearmonthday',resuser[b'id']+get_yearmonthday(respic[b'_datetimeoriginalsql'])) # 
    myappend(outlist,b'price',respic[b'id']) #
    myappend(outlist,b'ptitle',respic[b'_title']) #
    myappend(outlist,b'ptitle_idx',atpic.tokenizer.tokenize(respic[b'_title'])) #
    myappend(outlist,b'ptext_idx',atpic.tokenizer.tokenize(respic[b'_text'])) #
    myappend(outlist,b'timestamp',get_datexml(respic[b'_datetimeoriginalsql'])) # 
    myappend(outlist,b'mime',respic[b'_extension']) # 
    if respic[b'_exifgpslat']:
        if latlon_valid(respic[b'_exifgpslat'],respic[b'_exifgpslon']):
            # myappend(outlist,b'latlon_0_coordinate',respic[b'_exifgpslat']) # 
            # myappend(outlist,b'latlon_1_coordinate',respic[b'_exifgpslon']) # 
            lat=respic[b'_exifgpslat']
            lon=respic[b'_exifgpslon']
            outlist=mylatlon(lat,lon,outlist)
    elif resgallery[b'_lat']:
        if latlon_valid(resgallery[b'_lat'],resgallery[b'_lon']):
            # myappend(outlist,b'latlon_0_coordinate',resgallery[b'_lat']) #
            # myappend(outlist,b'latlon_1_coordinate',resgallery[b'_lon']) #
            lat=resgallery[b'_lat']
            lon=resgallery[b'_lon']
            outlist=mylatlon(lat,lon,outlist)
    for irandom in range(0,20):
        # randomnb=random.random() # uniform between 0.0 and 1.0
        # randomnb=atpic.mybytes.float2bytes(randomnb)
        maxint=pow(2,16) - 1 # short int
        randomnb=random.randint(0, maxint)
        randomnb=atpic.mybytes.int2bytes(randomnb)
        myappend(outlist,b'rand_'+atpic.mybytes.int2bytes(irandom),randomnb) # 
    picid=respic[b'id']
    uid=resuser[b'id']
    respictag=get_user_gallery_pic_tag(picid,uid)
    myappend(outlist,b'ptags',xml_concat(respictag))
    respicphrase=get_user_gallery_pic_phrase(picid,uid)
    myappend(outlist,b'pphrase',xml_concat(respicphrase))

    
    return (pid,outlist)

# ##############################
#  pic tag  elementary functions
# ##############################


def get_user_gallery_pic_tag(id,uid):
    yy=atpic.log.setname(xx,'get_user_gallery_pic_tag')
    query=b"select * from _user_gallery_pic_tag where _pic=$1 and _user=$2"
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',(id,uid))
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,result)
    return result

def xml_concat(respictag):
    yy=atpic.log.setname(xx,'xml_concat')
    outlist=[]
    tolist=[]
    for row in respictag:
        tolist.append(row[b'_text'])
    tolisttxt=b' '.join(tolist)

    # myappend(outlist,b'ptags',tolisttxt)
    output=myjoin(outlist)
    return output

# ##############################
#  pic phrase  elementary functions
# ##############################


def get_user_gallery_pic_phrase(id,uid):
    yy=atpic.log.setname(xx,'get_user_gallery_pic_phrase')
    query=b"select * from _user_gallery_pic_phrase where _pic=$1 and _user=$2"
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',(id,uid))
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,result)
    return result







# ##############################
#  gallery tag  elementary functions
# ##############################


def get_user_gallery_tag(id,uid):
    yy=atpic.log.setname(xx,'get_user_gallery_tag')
    query=b"select * from _user_gallery_tag where _gallery=$1 and _user=$2"
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',(id,uid))
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,result)
    return result
# ##############################
#  gallery phrase  elementary functions
# ##############################


def get_user_gallery_phrase(id,uid):
    yy=atpic.log.setname(xx,'get_user_gallery_phrase')
    query=b"select * from _user_gallery_phrase where _gallery=$1 and _user=$2"
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',(id,uid))
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,result)
    return result




# ################################
#  helper and recursive functions
# ################################

def allpics_user(uid):
    yy=atpic.log.setname(xx,'allpics_user')
    atpic.log.debug(yy,'input=',uid)
    userlist=get_user(uid)
    if not userlist:
        return []
    resuser=userlist[0]
    out_user=xml_user(resuser)
    atpic.log.debug(yy,'out_user',out_user)
    gallist=get_user_gallery_fromuser(uid)

    doclist=[]
    for resgallery in gallist:
        gid=resgallery[b'id']
        out_gallery=xml_user_gallery(resuser,resgallery)
        atpic.log.debug(yy,'out_gallery',out_gallery)

        atpic.log.debug(yy,'----gallery',gid)
        piclist=get_user_gallery_pic_fromgallery(gid,uid)
        for respic in piclist:
            out=[]
            atpic.log.debug(yy,'++++ pic')
            (pid,out_pic)=xml_user_gallery_pic(resuser,resgallery,respic)
            atpic.log.debug(yy,'out_pic=',out_pic)
            
            out=out_user+out_gallery+out_pic
            doclist.append((pid,myjoin(out)))
            

    return doclist

def allpics_user_gallery(gid,uid):
    yy=atpic.log.setname(xx,'allpics_user_gallery')
    gallerylist=get_user_gallery(gid,uid)
    resgallery=gallerylist[0]
    uid=resgallery[b'_user']

    userlist=get_user(uid)
    resuser=userlist[0]
    out_user=xml_user(resuser)
    out_gallery=xml_user_gallery(resuser,resgallery)

    piclist=get_user_gallery_pic_fromgallery(gid,uid)
    doclist=[]
    for respic in piclist:
        atpic.log.debug(yy,'++++ pic')
        out=[]
        (pid,out_pic)=xml_user_gallery_pic(resuser,resgallery,respic)
        
        out=out_user+out_gallery+out_pic
        doclist.append((pid,myjoin(out)))


    return doclist
    

def allpics_user_gallery_pic(pid,uid):
    yy=atpic.log.setname(xx,'allpics_user_gallery_pic')
    out=[]
    piclist=get_user_gallery_pic(pid,uid)
    respic=piclist[0]
    gid=respic[b'_gallery']

    gallerylist=get_user_gallery(gid,uid)
    resgallery=gallerylist[0]
    uid=resgallery[b'_user']

    userlist=get_user(uid)
    resuser=userlist[0]
    out_user=xml_user(resuser)
    out_gallery=xml_user_gallery(resuser,resgallery)
    # print('aaaa',pid)
    (pid,out_pic)=xml_user_gallery_pic(resuser,resgallery,respic)
    # print('aaaabb',pid)

    
    # out.append(out_user)
    # out.append(out_gallery)
    # out.append(out_pic)
    out=out_user+out_gallery+out_pic


    res=[]
    # print('cccc',out)
    res.append((pid, myjoin(out)))
    return res
    
# helper functions:
        
def get_user_gallery_fromuser(id):
    yy=atpic.log.setname(xx,'get_user_gallery_fromuser')
    query=b"select * from _user_gallery where _user=$1"
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',(id,))
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,result)
    return result

def get_user_gallery_pic_fromgallery(id,uid):
    yy=atpic.log.setname(xx,'get_user_gallery_pic_fromgallery')
    query=b"select * from _user_gallery_pic where _gallery=$1 and _user=$2"
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',(id,uid))
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,result)
    return result

# _user_gallery_pic_tag


# you have several solr object types:
# gallery (which includes gallery tags and phrases and license)
# pic (which includes gallery tags and phrases and license AND faces tags and phrases)
# you thus have two main entry points: 
# one for gallery with galleryid
# one for pic with picid
# this is very flexible, you could even cascade from gallery to pic 
# with a small perf hit

def solr_generate(atype,aid,uid):
    # in case of type user, repeat as argument the uid
    yy=atpic.log.setname(xx,'solr_generate')
    if atype==b'user':
        output=allpics_user(aid)
    elif atype==b'gallery':
        output=allpics_user_gallery(aid,uid) # gallery 1
    elif atype==b'pic':
        output=allpics_user_gallery_pic(aid,uid) # pic 1
    # output=b'<add>'+output+b'</add>'
    return (uid,output)

def print_json(output2):
    # prints a list of (pid,psource)
    # suitable for elasticsearch _bulk
    (uid,output)=output2
    jsonlist=[]
    for (pid,pic) in output:
        jsonlist.append(b'{ "index" : { "_id" : "'+pid+b'", "_routing" : "'+uid+b'"}}')
        jsonlist.append(b'{ '+pic+b' }')
    json=b'\n'.join(jsonlist)
    jsonutf8=json.decode("utf8")
    if jsonlist:
        print(jsonutf8)

if __name__ == "__main__":
    db=atpic.libpqalex.db()
    # output=solr_generate(b'user',b'2',b'2')
    # output=solr_generate(b'user',b'1',b'1')
    # output=solr_generate(b'gallery',b'1',b'1')
    # output=solr_generate(b'gallery',b'31384',b'7036')
    # output=solr_generate(b'pic',b'1',b'1')
    # output=solr_generate(b'user',b'128')
    # output=solr_generate(b'user',b'330')
    # print_json(output)

    # for (pid,pic) in output:
    #    print("+++++++++++++ pic",pid,"++++++++++++++")
    #     print(pic.decode("utf8"))
    # (path,pathtext,listdir,listfile,counter)=get_gallery_parents_path_recurse(b'1',b'1')
    # print(path)
    # print(pathtext)
    # print('listdir=',listdir)
    # print('listfile=',listfile)

    
    # for i in range(0,12050):
    for i in range(1,2):
        ib=atpic.mybytes.int2bytes(i)
        output=solr_generate(b'user',ib,ib)
        print_json(output)
    
