#!/usr/bin/python3
# interesting tag critics
# http://www.spiritedthought.com/2006/09/04/tag-clouds-of-today-are-so-yesturday/

import http.client
import random
import base64




import atpic.aperture
import atpic.coordinates
import atpic.dateutils
import atpic.forgesql
import atpic.hashat
import atpic.libpqalex
import atpic.log
import atpic.mybytes
import atpic.speed
import atpic.tokenizer
import atpic.randomalpha
import atpic.zmq_elastic_client

xx=atpic.log.setmod("DEBUG","elasticsearch_sql")

# sending SQL data to elasticsearch index

def forge_elasquery(uid,gid=b'',pid=b''):
    """
    should work even if gid='' but pid is defined
    """
    yy=atpic.log.setname(xx,'forge_elasquery')
    if gid:
        andgallery=b' AND _gallery=$'
        andgalleryid=b' AND id=$'
    else:
        andgallery=b''
        andgalleryid=b''

    if pid:
        andpicid=b' AND id=$'
        andpic=b' AND _pic=$'
    else:
        andpicid=b''
        andpic=b' AND _pic IN (SELECT pid FROM pp)'

        # andpic=b''

    query_args=[]
    queryb=[]
    queryb.append(b"WITH")
    
    queryu=[]
    queryu.append(b"uu AS (SELECT _user.id AS uid,_servershort AS servershort, _pricebase AS pricebaseu, _name AS username, _partition AS partition FROM _user WHERE _user.id=$ AND _user._deleted=0),")
    queryu.append(b"ua AS (SELECT _user,count(id) AS countua, string_agg(id::text,' ') as ufriend FROM _user_friend WHERE _user=$  GROUP BY _user),")
    
    for i in range(0,len(queryu)):
        query_args.append(uid)

    # gallery
    queryg=[]
    queryg.append(b"gg AS (SELECT id AS gid,_lat AS glat,_lon AS glon,_title AS gtitle, _text AS gtext, _mode AS gmode,_path AS gpath, _pricebase AS pricebaseg FROM _user_gallery WHERE _user=$"+andgalleryid+b" AND _deleted=0),")
    queryg.append(b"gt AS (SELECT _gallery,count(id) AS countgt, string_agg(_text,' ') as gtag FROM _user_gallery_tag WHERE _user=$"+andgallery+b" GROUP BY _gallery),")
    queryg.append(b"gf AS (SELECT _gallery,count(id) AS countgf, string_agg(_text,' ') as gphrase FROM _user_gallery_phrase WHERE _user=$"+andgallery+b" GROUP BY _gallery),")
    queryg.append(b"ga AS (SELECT _gallery,count(id) AS countga, string_agg(id::text,' ') as gfriend FROM _user_gallery_friend WHERE _user=$"+andgallery+b" GROUP BY _gallery),")
    
    for i in range(0,len(queryg)):
        query_args.append(uid)
        if gid:
            query_args.append(gid)
    
    # picture
    queryp=[]
    queryp.append(b"pp AS (SELECT id AS pid,_extension AS extension, _exifgpslat AS plat,_exifgpslon AS plon,_title AS ptitle, _text AS ptext, _datetimeoriginalsql AS datetimeoriginalsql,_mimetype_magic AS mimetype_magic, _mimesubtype_magic AS mimesubtype_magic, _mimetype_exiftool AS mimetype_exiftool, _mimesubtype_exiftool AS mimesubtype_exiftool, _exifmake AS exifmake, _exifmodel AS exifmodel, _exifaperture AS exifaperture, _exifexposuretime AS exifexposuretime, _exiffocallength AS exiffocallength, _originalname AS originalname,_counter AS counter,_pricebase AS pricebasep, _width AS width, _height AS height, _duration AS duration, _user,_gallery FROM _user_gallery_pic WHERE _user=$"+andgallery+andpicid+b" AND _deleted=0),")

    queryp.append(b"pa AS (SELECT _pic,string_agg(_code||';'|| _extension||';'|| _pathstore ||';'||_pic::text||';'||_datestore::text ,'|') as partefact FROM _user_gallery_pic_artefact WHERE _user=$"+andpic+b" GROUP BY _pic),")
    queryp.append(b"pt AS (SELECT _pic,count(id) AS countpt, string_agg(_text,' ') as ptag FROM _user_gallery_pic_tag WHERE _user=$"+andpic+b" GROUP BY _pic),")
    queryp.append(b"ph AS (SELECT _pic,count(id) AS countph, string_agg(_path,'|') as ppath FROM _user_gallery_pic_path WHERE _user=$"+andpic+b" GROUP BY _pic),")
    queryp.append(b"pf AS (SELECT _pic,count(id) AS countpf, string_agg(_text,' ') as pphrase FROM _user_gallery_pic_phrase WHERE _user=$"+andpic+b" GROUP BY _pic),")
    # queryp.append(b"pa AS (SELECT _pic,count(id) AS countpa, string_agg(id::text,' ') as pfriend FROM _user_gallery_pic_friend WHERE _user=$"+andpic+b" GROUP BY _pic),")
    queryp.append(b"pv AS (SELECT _pic,count(id) AS countpv, avg(_score) as pvote FROM _user_gallery_pic_vote WHERE _user=$"+andpic+b" GROUP BY _pic),")
    
    query_args.append(uid)
    if andgallery:
        query_args.append(gid)
    if andpicid:
        query_args.append(pid)
        
    for i in range(1,len(queryp)):
        query_args.append(uid)
        if pid:
            query_args.append(pid)

    

    queryend=[]
    queryend.append(b"re AS (SELECT pp.*,gg.* ,gt.*,pt.*,uu.* ,gf.*,pf.*,ph.*,ua.*,ga.*,pv.*,pa.* FROM pp LEFT JOIN gg ON pp._gallery=gg.gid LEFT JOIN gt ON gt._gallery=pp._gallery LEFT JOIN pt ON pt._pic=pp.pid LEFT JOIN uu ON uu.uid=pp._user LEFT JOIN gf ON gf._gallery=pp._gallery LEFT JOIN  pf ON pf._pic=pp.pid LEFT JOIN ua ON ua._user=pp._user LEFT JOIN ph ON ph._pic=pp.pid LEFT JOIN ga ON ga._gallery=gg.gid LEFT JOIN pv ON pv._pic=pp.pid LEFT JOIN pa ON pa._pic=pp.pid)")
    queryend.append(b"SELECT uid,gid,pid,extension,servershort,username,partition,gmode,gpath,ppath,ufriend,gfriend,gtag,ptag,gphrase,pphrase,glat,glon,plat,plon,gtitle,ptitle,gtext,ptext,datetimeoriginalsql,mimetype_magic, mimesubtype_magic, mimetype_exiftool, mimesubtype_exiftool, exifmake, exifmodel, exifaperture, exifexposuretime, exiffocallength, originalname , counter, width, height, duration, countpt,countph,countpf, countgt, countgf, countga, countua,countpv,pvote,pricebasep,pricebaseg,pricebaseu,partefact FROM re")
    


    query_all=queryb+queryu+queryg+queryp+queryend
    query_string=b'\n'.join(query_all)
    (query_string,query_args)=atpic.forgesql.transform(query_string,query_args)
    atpic.log.debug(yy,"++++++++++++++++++++++")
    atpic.log.debug(yy,query_string.decode('utf8'))
    atpic.log.debug(yy,query_args)
    atpic.log.debug(yy,"----------------------")
    return (query_string,query_args)
    


def forge_elasquery_path(uid,gid=b''):
    query_args=[]
    query_args.append(uid)
    if gid!=b'':
        andg=b' AND id=$'
        query_args.append(gid)
    else:
        andg=b''
    query_string=b"SELECT id as gid,_user as uid,_path as path FROM _user_gallery WHERE _user=$ AND _deleted=0"+andg
    (query_string,query_args)=atpic.forgesql.transform(query_string,query_args)
    return (query_string,query_args)

def forge_elasquery_vpath(uid,pid=b''):
    query_args=[]
    query_args.append(uid)
    if pid!=b'':
        andp=b' AND _pic=$'
        query_args.append(pid)
    else:
        andp=b''
    query_string=b"SELECT _user as uid, _path as path FROM _user_gallery_pic_path WHERE _user=$"+andp
    (query_string,query_args)=atpic.forgesql.transform(query_string,query_args)
    return (query_string,query_args)


"""
# GROUP BY string aggregate http://www.postgresql.org/docs/9.1/static/functions-aggregate.html

# counters are used to calculate the popularity, with vote

"""

def mycallback_simple(i,row,essock):
    # used to debug only:
    # doesnothing, just logs to the logs
    yy=atpic.log.setname(xx,'mycallback_simple')
    atpic.log.info(yy,i,row)
    # 

def mycallback(i,row,essock):
    yy=atpic.log.setname(xx,'mycallback')
    atpic.log.debug(yy,'input=',(i,row))
    # 
    [uid,pid,ajson]=dic2json(row)
    atpic.log.debug(yy,'routing',uid,'pid',pid,'json=\n',ajson.decode('utf8'))
    # at this stage you need to post to elastic search
    uri=b'/atpic/pic/'+pid+b'?routing='+uid
    content=atpic.zmq_elastic_client.http_general(essock,b'PUT',uri,ajson)


def mycallback_path(i,row,essock):
    mycallback_gallery_both(i,row,b'path',essock)

def mycallback_vpath(i,row,essock):
    mycallback_gallery_both(i,row,b'vpath',essock)

def mycallback_gallery_both(i,row,gallerytype,essock):
    # if we want to know in advance the facets
    # we need to be able to make a quick call
    # for path somepath, give the facets (possible subpath)
    
    # two techniques:
    # 1) one store in one document all the facets
    # 2) make a search
    #  solution 2) is better:
    # for a gallery path: /france/paris/eiffel
    # store the document with that ID 
    # (base64 encoded without slash as elasticsearch does not accept it)
    # and explode /france, /france/paris, /france/paris/eiffel
    # same thing for pics
    # for pics it is more difficult to delete:
    # may need from time to time to clean for a user
    # and repost all pics vpath
    # override at each post
    # not really a pb if we have more path that give zero results (at least in vpath)
    # then that requires a facet but the size is the gallery nb << pic nb
    # 
    # OR
    # /countries [france,usa,etc..]
    # /countries/france [paris, lyon, marseille]
    #
    # OR: 
    # SQL
    # 
    # OR:
    # one path //frace/paris/eiffel
    # gives seveal documents
    # /france [parent:/ , uid:1]
    # /france/paris [ parent: /france, uid:1 ]
    # /france/paris/eiffel [ parent: /france/paris , uid:1] 

    yy=atpic.log.setname(xx,'mycallback_gallery_both')
    atpic.log.debug(yy,i,row)
    uid=row[b'uid']
    path=row[b'path']
    atpic.log.debug(yy,'path',path)
    altchars=b"-_"

    # would need to clean
    # curl 'http://localhost:9200/atpic/path/_search?q=uid:1&size=100' | json_reformat 
    # curl -XDELETE 'http://localhost:9200/atpic/path/_query?q=uid:1&routing=1'

    if path==b'':
        pass # this is the root gallery and it has no parent
    else:
        splitted=path.split(b'/')
        newl=[]
        for ele in splitted:
            parent=b'/'.join(newl)
            newl.append(ele)
            subpath=b'/'.join(newl)
            atpic.log.debug(yy,'(subpath=parent+ele)',(subpath,parent,ele))
            pathbase64=base64.b64encode(subpath,altchars)
            uri=b'/atpic/'+gallerytype+b'/'+pathbase64+b'?routing='+uid
            atpic.log.debug(yy,'uri',uri)
            ajson=b'{ "uid" : '+uid+b', "parent" : "'+parent+b'", "path" : "'+subpath+b'"}'
            atpic.log.debug(yy,ajson)
            content=atpic.zmq_elastic_client.http_general(essock,b'PUT',uri,ajson)
            atpic.log.debug(yy,content)




def set_popularity(row):
    """
    Computes the popularity score from the counts and votes
    """
    yy=atpic.log.setname(xx,'set_popularity')
    popularity= \
        atpic.mybytes.bytes2float(row[b'countgt']) \
        + atpic.mybytes.bytes2float(row[b'countpt']) \
        + atpic.mybytes.bytes2float(row[b'countgf']) \
        + atpic.mybytes.bytes2float(row[b'countpf']) \
        + atpic.mybytes.bytes2float(row[b'countga']) \
        + atpic.mybytes.bytes2float(row[b'countpv']) \
        + atpic.mybytes.bytes2float(row[b'counter'])

    return popularity

def set_price(row):
    """
    Computes the price score from the counts and votes
    """
    yy=atpic.log.setname(xx,'set_price')
    if row[b'pricebasep']:
        pricebase=atpic.mybytes.bytes2float(row[b'pricebasep']) # take the pic base price
    elif  row[b'pricebaseg']:
        pricebase=atpic.mybytes.bytes2float(row[b'pricebaseg']) # take the gallery base price
    elif  row[b'pricebaseu']:
        pricebase=atpic.mybytes.bytes2float(row[b'pricebaseu']) # take the user base price
    else:
        pricebase=1.0 # a default value
    # then on top of base price, increase the price to pay a commission to taggers
    price= \
        + 0.03 * atpic.mybytes.bytes2float(row[b'countgt']) \
        + 0.30 * atpic.mybytes.bytes2float(row[b'countpt']) \
        + 0.03 * atpic.mybytes.bytes2float(row[b'countgf']) \
        + 0.30 * atpic.mybytes.bytes2float(row[b'countpf'])

    return price


def latlon_valid(lat,lon):
    """
    Solr validates, so we need to make sure it is valid
    """
    yy=atpic.log.setname(xx,'latlon_valid')
    atpic.log.debug(yy,'input',lat,lon)
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
    atpic.log.debug(yy,'valid is:', valid)
    return valid


def array_2json_array(alist):
    # this is a list
    yy=atpic.log.setname(xx,'array_2json_array')
    newlist=[]
    for el in alist:
        newlist.append(b'"'+el+b'"')

    newarray=b','.join(newlist)

    return newarray

def string_2json_array(friends):
    """
    Takes a bytes string with spaces and returns a json formatted array
    """
    yy=atpic.log.setname(xx,'string_2json_array')
    friends_list=friends.split()
    friends_list2=[]
    for af in friends_list:
        friends_list2.append(b'"'+af+b'"')
    friends_str=b','.join(friends_list2)
    atpic.log.debug(yy,'friends_str',friends_str)
    return friends_str


def coord_set(row,ajson):
    yy=atpic.log.setname(xx,'coord_set')
    atpic.log.debug(yy,'input',row[b'plat'],row[b'plon'],row[b'glat'],row[b'glon'])
    hasgeo=0
    if row[b'plat']:
        if latlon_valid(row[b'plat'],row[b'plon']):
            lat=row[b'plat']
            lon=row[b'plon'] 
            hasgeo=1
    elif row[b'glat']:
        if latlon_valid(row[b'glat'],row[b'glon']):
            lat=row[b'glat']
            lon=row[b'glon']
            hasgeo=1
    if hasgeo:
        atpic.log.debug(yy,'hascoord',(lon,lat))
        ajson.append(b'"location" : { "lat" : '+lat+b', "lon" : '+lon+b'},') 
        
        # ============================================   

        loni=atpic.mybytes.bytes2float(lon)
        lati=atpic.mybytes.bytes2float(lat)
        for wlen in range(2,26):
            ((lonb,lonb1),(lonbf,lonb1f))=atpic.coordinates.get_one_interval(loni,wlen,maxcoord=180)
            ((latb,latb1),(latbf,latb1f))=atpic.coordinates.get_one_interval(lati,wlen,maxcoord=90)
            packed=atpic.coordinates.pack(lonb,latb,wlen)
            ajson.append(b'"coord_'+atpic.mybytes.int2bytes(wlen)+b'" : "'+atpic.mybytes.int2bytes(packed)+b'",')

            # ajson.append(b'"lon_'+atpic.mybytes.int2bytes(wlen)+b'" : "'+atpic.mybytes.int2bytes(lonb)+b'",') 
            # ajson.append(b'"lat_'+atpic.mybytes.int2bytes(wlen)+b'" : "'+atpic.mybytes.int2bytes(latb)+b'",') 
        # ============================================   

    else:
        atpic.log.debug(yy,'hasnocoord')
    return ajson



def dic2json(row):
    # can be unit tested
    """
    Transforms a dict into a json, with uid and pid (to use in URI)
    Computes the popularity score from the counts and votes
    Computes the price
    (and user reputation?)
    Pre-tokenize: path, tags, phrases
    """
    yy=atpic.log.setname(xx,'dic2json')
    uid=row[b'uid']
    pid=row[b'pid']

    ajson=[]
    ajson.append(b'{')
    ajson.append(b'"username" : "'+row[b'username']+b'",')
    ajson.append(b'"servershort" : "'+row[b'servershort']+b'",')
    # popularity
    popularity=set_popularity(row)
    ajson.append(b'"popularity" : "'+atpic.mybytes.float2bytes(popularity)+b'",')
    # set price
    price=set_price(row)
    # may want to save back price into SQL
    ajson.append(b'"price" : "'+atpic.mybytes.float2bytes(price)+b'",')
    # latitude and longitude

    # permissions and friends
    ajson.append(b'"mode" : "'+row[b'gmode']+b'",')
    friends=row[b'ufriend']+b' '+row[b'gfriend']
    ajson.append(b'"friends" : ['+string_2json_array(friends)+b'],')

    # tags
    tagall=row[b'gtag']+b' '+row[b'ptag']
    # ajson.append(b'"tags" : "'+atpic.tokenizer(tagall)+b'",')


    # phrases: indexed but not stored:
    phrases_all=row[b'gphrase']+b' '+row[b'pphrase']+b' '+row[b'gtext']+b' '+row[b'gtitle']+b' '+row[b'ptext']+b' '+row[b'ptitle']+b' '+tagall+b' '+row[b'gpath']+b' '+row[b'originalname']+b' '+row[b'ppath']
    catch_all=atpic.tokenizer.tokenize(phrases_all)
    # need to clean and normalize
    # we put tags and phrases and description into one BIG field: phrases
    # catchall
    ajson.append(b'"phrases" : "'+catch_all+b'",')



    ajson=coord_set(row,ajson)

    

    # again but stored not tokenized and not indexed:
    ajson.append(b'"gtitle" : "'+row[b'gtitle']+b'",')
    ajson.append(b'"ptitle" : "'+row[b'ptitle']+b'",')


    # date (need facetting)
    # to build the URLs: (store dates and extension)
    # ajson.append(b'"datetime" : "'+atpic.dateutils.date_sql2iso(row[b'datetimeoriginalsql'])+b'",')
    # put the user ID in the facets as without it it could lead to huge
    # number of documents per term (problem?), it is more the nb of facets
    if row[b'datetimeoriginalsql']!=b'':
        ajson.append(b'"year" : "'+atpic.dateutils.date_sqlyear(row[b'datetimeoriginalsql'])+b'",')
        ajson.append(b'"yearmonth" : "'+atpic.dateutils.date_sqlyearmonth(row[b'datetimeoriginalsql'])+b'",')
        ajson.append(b'"yearmonthday" : "'+atpic.dateutils.date_sqlyearmonthday(row[b'datetimeoriginalsql'])+b'",')
        ajson.append(b'"yearmonthdaytime" : "'+atpic.dateutils.date_sql2elastic(row[b'datetimeoriginalsql'])+b'",')
    ajson.append(b'"extension" : "'+row[b'extension']+b'",')

    # mimes
    ajson.append(b'"mimetype" : "'+row[b'mimetype_exiftool']+b'",')
    ajson.append(b'"mimesubtype" : "'+row[b'mimesubtype_exiftool']+b'",')
    # some fun exif data
    if atpic.aperture.f4elasticsearch(row[b'exifaperture']) != b'':
        ajson.append(b'"f" : "'+atpic.aperture.f4elasticsearch(row[b'exifaperture'])+b'",')
    ajson.append(b'"make" : "'+row[b'exifmake']+b'",')
    ajson.append(b'"focallength" : "'+row[b'exiffocallength']+b'",')
    ajson.append(b'"model" : "'+row[b'exifmodel']+b'",')
    if row[b'exifexposuretime'] != b'':
        ajson.append(b'"speed" : "'+atpic.speed.speed4elasticsearch(row[b'exifexposuretime'])+b'",')

    ajson.append(b'"width" : "'+row[b'width']+b'",')
    ajson.append(b'"height" : "'+row[b'height']+b'",')
    ajson.append(b'"duration" : "'+row[b'duration']+b'",')


    # artefacts
    artefact=row[b'partefact']
    if artefact!=b'':
        artefacts=artefact.split(b'|')
        for anartefact in artefacts:
            artedetails=anartefact.split(b';')
            resolutioncode=artedetails[0]
            extension=artedetails[1]
            pathondisk=artedetails[2]
            pid=artedetails[3]
            hashvalue=atpic.hashat.dohash(pid,resolutioncode,pathondisk)
            hashvalue=row[b'partition']+hashvalue+b'.'+extension
            hashkey=b'pathstore_'+resolutioncode
            # newdict[hashkey]=hashvalue
            ajson.append(b'"'+hashkey+b'" : "'+hashvalue+b'",')





    # randomness
    # randbitsnb=16 # short int
    # maxint=pow(2,randbitsnb-1) - 1 # short int
    # minint=-pow(2,randbitsnb-1)  # short int
    # for irandom in range(0,20):
    #     randomnb=random.randint(minint, maxint)
    #     randomnb=atpic.mybytes.int2bytes(randomnb)
    #     ajson.append(b'"rand_'+atpic.mybytes.int2bytes(irandom)+b'" : "'+randomnb+b'",') # 
    # new random (no sort by which requires more? memory)
    ajson.append(b'"randoms" : "'+atpic.randomalpha.store()+b'",') # 

    # filename
    ajson.append(b'"originalname" : "'+row[b'originalname']+b'",')

    # dirs and vdirs
    ajson.append(b'"gpath" : "'+row[b'gpath']+b'",')
    
    if row[b'ppath']!=b'':
        ppath_array=row[b'ppath'].split(b'|')
        pparray=array_2json_array(ppath_array)
        ajson.append(b'"ppath" : ['+pparray+b'],') # an array

    # then explode dirs and vdirs
    gpath_dirs=row[b'gpath'].strip(b'/').split(b'/')
    cumulpath=b''
    i=0
    for abase in gpath_dirs:
        cumulpath=cumulpath+b'/'+abase
        ajson.append(b'"dir_'+atpic.mybytes.int2bytes(i)+b'" : "'+cumulpath+b'",') # an array
        i=i+1
    # explode vdirs
    # transforsm
    # /best/smiles,/best/landscape,/colors into d_0[/best,/colors], d_1[/best/smiles,/best/landscape]
            
    if row[b'ppath']!=b'':
        # first get the maximum lenght
        amax=0
        for vdir in ppath_array:
            vdirs_ar=vdir.strip(b'/').split(b'/')
            alen=len(vdirs_ar)
            if alen> amax:
                amax=alen
        # then allocate the memory:
        alld={}
        for i in range(0,amax):
            alld[i]={} # dictionarry to automatically remove duplicates
        # then populate the lists
        for vdir in ppath_array:
            gpath_dirs=vdir.strip(b'/').split(b'/')
            cumulpath=b''
            i=0
            for abase in gpath_dirs:
                cumulpath=cumulpath+b'/'+abase
                alld[i][cumulpath]=1
                i=i+1
        # finally, display the lists
        for i in range(0,amax):
            ajsonel=[]
            for key in alld[i].keys():
                ajsonel.append(b'"'+key+b'"')
            ajson.append(b'"vdir_'+atpic.mybytes.int2bytes(i)+b'" : ['+b','.join(ajsonel)+b'],')



    # finish with the one you will always output and no worries about the last coma
    ajson.append(b'"uid" : "'+row[b'uid']+b'",')
    ajson.append(b'"gid" : "'+row[b'gid']+b'",')
    ajson.append(b'"pid" : "'+row[b'pid']+b'"') # last one has NO coma
    ajson.append(b'}')
    return [uid,pid,b'\n'.join(ajson)]


def doindex_pic(uid,gid,pid,db,essock):
    """
    pid
    or
    gid,pid
    could be b''
    """
    yy=atpic.log.setname(xx,'doindex_pic')
    atpic.log.debug(yy,"input:",(uid,gid,pid))
    (query_string,query_args)=forge_elasquery(uid,gid,pid)
    atpic.log.debug(yy,"(query_string,query_args)",(query_string,query_args))
    ps=atpic.libpqalex.pq_prepare(db,b'',query_string)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',query_args) # query_args is a list
    atpic.libpqalex.process_result_with_callback(result,mycallback,essock)
    atpic.log.debug(yy,"indexing sent")




def doindex_path(uid,gid,pid,db,essock):
    """
    pid
    or
    gid,pid
    could be b''
    """
    yy=atpic.log.setname(xx,'doindex_path')
    atpic.log.debug(yy,"input:",(uid,gid,pid))
    (query_string,query_args)=forge_elasquery_path(uid,gid)
    atpic.log.debug(yy,"(query_string,query_args)=",(query_string,query_args))
    ps=atpic.libpqalex.pq_prepare(db,b'',query_string)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',query_args) # query_args is a list
    atpic.libpqalex.process_result_with_callback(result,mycallback_path,essock)



def doindex_vpath(uid,gid,pid,db,essock):
    """
    pid
    or
    gid,pid
    could be b''
    """
    yy=atpic.log.setname(xx,'doindex_vpath')
    atpic.log.debug(yy,"input:",(uid,gid,pid))
    (query_string,query_args)=forge_elasquery_vpath(uid,pid)
    atpic.log.debug(yy,"(query_string,query_args)=",(query_string,query_args))
    ps=atpic.libpqalex.pq_prepare(db,b'',query_string)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',query_args) # query_args is a list
    atpic.libpqalex.process_result_with_callback(result,mycallback_vpath,essock)



if __name__ == "__main__":
    inputs=(
        # (b'1',b'1',b'1'),
        # (b'1',b'22',b''),
        # (b'1',b'22',b'333'),

        (b'1',b'',b'1'),
        )
    


    # ==============
    # to to a FULL reindex (re-index), run this script for all users
    # you can use 'screen', to launch over ssh as it is a very long job
    inputs=[]
    # for i in range(1,12821):
    for i in range(1,2):
        inputs.append((atpic.mybytes.int2bytes(i),b'',b''))
    

        
    db=atpic.libpqalex.db_native()
    essock=atpic.zmq_elastic_client.connect_first()
    

    for (uid,gid,pid) in inputs:
        print("DOING",(uid,gid,pid))
        doindex_pic(uid,gid,pid,db,essock)
        # doindex_path(uid,gid,pid,db,essock)
        # doindex_vpath(uid,gid,pid,db,essock)



