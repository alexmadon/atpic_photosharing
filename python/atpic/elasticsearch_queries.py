#!/usr/bin/python3

# this files defines all the functions that create the json 
# to be sent at query time to elasticsearch
# for contentcreation time, see elasticesearch_sql

# facet queries load the whole index into memory
# we could avoid facets as we know in advance the facet names
# (dates by URL, path in SQL, geo square)
import calendar
import time
import datetime
import random
import re
import traceback

import atpic.log
import atpic.tokenizer
import atpic.mybytes
import atpic.queryparser
import atpic.zmq_elastic_client
import atpic.aperture
import atpic.speed
import atpic.dateutils
import atpic.jsonat_json2python
import atpic.coordinates
import atpic.randomalpha

xx=atpic.log.setmod("INFO","elasticsearch_queries")

# ====================================================
# 
#  queryparser: parsed query to json: 3nd parsing
#
# =====================================================
# transforms to json



# ==============================================================
#
#     permission function common to search and facets
#
# ===============================================================

def forge_permission_filter(aid):
    # authenticated id an permissions
    # we will need to parse the json output and may present only watermarked
    yy=atpic.log.setname(xx,'forge_permission_filter')
    atpic.log.debug(yy,"input=",aid)
    if aid==b'':
        andpermission=b'{"or" : [ {"term" : {"mode" : "b"}}, {"term" : {"mode" : "t"}} , {"term" : {"mode" : "s"}} ]}' # public or protect or sell
    else:
        # surfer is authenticated
        ap=[]
        ap.append(b'{"or" : [ ')
        ap.append(b'{"or" : [ {"term" : {"mode" : "b"}}, {"term" : {"mode" : "t"}} , {"term" : {"mode" : "s"}} ]},') # public, protect, sell
        ap.append(b'{"and" : [{"term" : {"mode" : "v" }} , {"term" : {"uid" : "'+aid+b'" }}]}, ') # private and owner
        ap.append(b'{"and" : [{"term" : {"mode" : "f" }} , {"term" : {"friends" : "'+aid+b'" }}]} ') # friend mode and surfer is a friend
        ap.append(b']}')
        andpermission=b''.join(ap)
    atpic.log.debug(yy,"output=",)
    return andpermission

def get_fields():
    # datestore etc are used to create the idbased URL
    yy=atpic.log.setname(xx,'get_fields')
    return b'["uid","gid","pid","servershort","gtitle","ptitle","originalname","price","location.lon","location.lat","yearmonthdaytime","pathstore","pathstore_r70","pathstore_r160","pathstore_r350","pathstore_r600","pathstore_r1024","pathstorewater_r350","pathstorewater_r600","width","height","duration","mode","_source"]'
    # uid is necessary for permission checks


# ==========================================================
#
#     1) general query parser for search
#
# ==========================================================

# ======================================================
#                     sort
# ======================================================


def set_sort_random():
    yy=atpic.log.setname(xx,'set_sort_random')
    atpic.log.debug(yy,"input=",)
    rndlist=atpic.randomalpha.search()
    tmpl=[]
    for rndc in rndlist:
        tmpl.append(b'{"term" : { "randoms": "'+rndc+b'" }}')
        # this needs to be ad to the QUERY!!!!
        # a=b'{"query" : {"bool": {"must" : [{"term": {"randoms": "a"}},{"term": {"randoms": "b"}}] }},"size" : 1}'
    out=b'{"bool": {"must" : ['+b', '.join(tmpl)+b']}}'
    atpic.log.debug(yy,"output=",out)
    return out

def set_sort(parsed):
    """
    "sort" : [
        { "post_date" : {"order" : "asc"} },
        "user",
        { "name" : "desc" },
        { "age" : "desc" },
        "_score"
    ],
    """
    yy=atpic.log.setname(xx,'set_sort')
    atpic.log.debug(yy,"input=",parsed)
    asort=b''
    outl=[]
    for ele in parsed:
        (asign,atype,avalue)=ele
        if asign==b'+' and atype in [b'sort',b'orderby',]:
            if avalue==b'random':
                pass # this is processed at the query level
            elif avalue in [b'price',b'price_asc']:
                outl.append(b'{ "price" : "asc" }')
            elif avalue in [b'price_desc']:
                outl.append(b'{ "price" : "desc" }')
            elif avalue in [b'popularity',b'popularity_desc']:
                outl.append(b'{ "popularity" : "desc" }')
            elif avalue in [b'popularity_asc']:
                outl.append(b'{ "popularity" : "asc" }')
            elif avalue in [b'date',b'date_desc']:

                # http://www.elasticsearch.org/guide/reference/mapping/core-types.html
                # The date type is a special type which maps to JSON string type. It follows a specific format that can be explicitly set. All dates are UTC. Internally, a date maps to a number type long, with the added parsing stage from string to long and from long to string. 
                # The date type will also accept a long number representing UTC milliseconds since the epoch, regardless of the format it can handle.

                # http://lucene.apache.org/core/old_versioned_docs/versions/3_0_1/api/all/org/apache/lucene/document/DateTools.html
                # Provides support for converting dates to strings and vice-versa. The strings are structured so that lexicographic sorting orders them by date, which makes them suitable for use as field values and search terms.

                # http://stackoverflow.com/questions/12513145/string-lexicographic-range-query-in-elasticsearch
                # ---- conclusion ----
                # could store date as string
                # or as long
                outl.append(b'{ "yearmonthdaytime" : "desc" }')
            elif avalue in [b'date_asc']:
                outl.append(b'{ "yearmonthdaytime" : "asc" }')
            elif avalue in [b'relevance']:
                outl.append(b'"_score"')
    if len(outl)>0:
        asorts=b', '.join(outl)
        asort=b'"sort" : ['+asorts+b']'
    atpic.log.debug(yy,"output=",asort)
    return asort





def get_path(atype,avalue):
    # atype can be b'path' or b'vpath', not used
    # avalues can be 
    #       alex/nathalie
    #       /nathalie
    #       alex/nathalie/*
    #       /nathalie/*
    # retruns a list of (field,term)
    yy=atpic.log.setname(xx,'get_path')
    atpic.log.debug(yy,"input=",(atype,avalue))
    pathlist=[]

    # user part
    if not avalue.startswith(b'/'):
        splitted=avalue.split(b'/')
        pathvalue=b'/'+b'/'.join(splitted[1:])
        pathlist.append((b'servershort',splitted[0]))
    else:
        pathvalue=avalue
    # what if more than one path????? 
    if atype==b'tree':
        exactmatch=b'gpath'
        submatch=b'dir_'
    elif atype==b'vtree':
        exactmatch=b'ppath'
        submatch=b'vdir_'

    # path part
    if pathvalue.endswith(b'/*'):
        # match subdirs too
        pathvalue=pathvalue[:len(pathvalue)-2]
        slash_nb=pathvalue.count(b'/')
        if slash_nb>0:
            pathlist.append((submatch+atpic.mybytes.int2bytes(slash_nb-1),pathvalue))
        else:
            atpic.log.debug(yy,"this is the root dir, not worth filtering")

    else:
        # exact match
        pathvalue=pathvalue[1:]
        pathlist.append((exactmatch,pathvalue))

    
        

    atpic.log.debug(yy,"output=",pathlist)
    return pathlist

def identity(x):
    return x

    



def process_one_condition(asign,atype,avalue,outqp,outqm,outfp,outfm):
    # input:
    # =========
    # a condition (asign,atype,avalue) and three lists:
    # outqp=[] # out query +
    # outqm=[] # out query -
    # outfp=[] # out filter list +
    # outfm=[] # out filter list -
    # output: 
    # =========
    # the three list modified
    yy=atpic.log.setname(xx,'process_one_condition')
    atpic.log.debug(yy,"input=",(asign,atype,avalue,outqp,outqm,outfp,outfm))

    typemap={
        b'aperture':b'f',
        b'exposuretime':b'speed',
        b'Type':b'mimetype',
        b'type':b'mimesubtype',
        b'Filetype':b'mimetype',
        b'filetype':b'mimesubtype',
        b'filename':b'originalname',
        b'dns':b'servershort',
        }

    atpic.log.debug(yy,(asign,atype,avalue))
    mytype=typemap.get(atype,atype) # allow type mapping


    try:

        # through away sorting as this is dealt by somewhere else
        if atype in [b'sort',b'orderby']:
            # do only the random sort that is dealt at the query level (not the sort or filter level)
            outrandom=set_sort_random()
            outqp.append(outrandom)
        elif atype in [b'lat',b'lon']:
            pass
        # deal with words
        elif atype==b'word':
            outq=b''
            mytype=b'phrases'
            # http://localhost:9999/guide/reference/query-dsl/bool-query.html
            # http://localhost:9999/guide/reference/query-dsl/match-query.html
            atpic.log.debug(yy,'this is a word')
            # normalize
            # the check there is spaces to know if it is a term
            # or a phrase
            # tokenize (insert white space in chinese and japanese and thai and 
            # normalize and lowercase
            avalue=atpic.tokenizer.tokenize(avalue)
            space_nb=avalue.count(b' ')
            if space_nb>0:
                atpic.log.debug(yy,'there are spaces',space_nb)
                outq+=b'{ "match_phrase" : { "'+mytype+b'" : "'+avalue+b'"}}'
            else:
                atpic.log.debug(yy,'there are no spaces')
                outq+=b'{ "term" : { "'+mytype+b'" : "'+avalue+b'"}}'
            

            # append to the relevant list
            if asign==b'-':
                outqm.append(outq)
            else:
                outqp.append(outq)


        # for filter we use 'and' which performs better than 'bool'
        else:
            atpic.log.debug(yy,'this is not a word')
            outf=b''
            # now depends on types:
            if atype in [b'uid',b'gid',b'pid',b'Type',b'type',b'Filetype',b'filetype',b'filename',b'username',b'dns']:
                atpic.log.debug(yy,'we just pipe the value without modification')
                outf+=b'{"term" : { "'+mytype+b'" : "'+avalue+b'"}}'
            elif atype==b'packedcoord':
                (packed,resolution)=avalue.split(b'.')  # packedcoord:1234.23
                outf+=b'{ "term" : { "coord_'+resolution+b'" : "'+packed+b'" }}'
            elif atype in (b'geopathexact',b'geoexact'):
                (xmin,xmax,ymin,ymax)=geopath2bounds(avalue)
                (packed,resolution)=atpic.coordinates.identify_bounds2facet(xmin,xmax,ymin,ymax)
                resolution=atpic.mybytes.int2bytes(resolution)
                packed=atpic.mybytes.int2bytes(packed)
                outf+=b'{ "term" : { "coord_'+resolution+b'" : "'+packed+b'" }}'

            elif atype in (b'geopath',b'geo'):
                (xmin,xmax,ymin,ymax)=geopath2bounds(path)
                (outqp,outqm,outfp,outfm)=add_coordinates_filter2(xmin,xmax,ymin,ymax,outqp,outqm,outfp,outfm)
            elif atype in (b'geopackpath',b'geopack'):
                [empty,resolution,lonb,latb]=avalue.split(b'/')  # packedcoord:8/124/456
                lonbi=atpic.mybytes.bytes2int(lonb)
                latbi=atpic.mybytes.bytes2int(latb)
                resolutioni=atpic.mybytes.bytes2int(resolution)
                packedi=atpic.coordinates.pack(lonbi,latbi,resolutioni)
                packed=atpic.mybytes.int2bytes(packedi)
                atpic.log.debug(yy,'packed',packed)
                outf+=b'{ "term" : { "coord_'+resolution+b'" : "'+packed+b'" }}'
            elif atype in [b'model',b'make',]: # this is text like
                tokenized_value=atpic.tokenizer.tokenize(avalue)
                splitted_value=tokenized_value.split()
                text_like=[]
                for aterm in splitted_value:
                    text_like.append(b'{"term" : { "'+mytype+b'" : "'+aterm+b'"}}')
                outf+=b', '.join(text_like)
            elif atype in [b'tree',b'vtree',]:
                # alex/italia2006
                # /italia2006
                # /italia2006/*
                # alex/italia2006/*
                pathlist=get_path(atype,avalue)
                if len(pathlist)==2:
                    suboutf=[]
                    for  (mytype,myvalue) in pathlist:
                        suboutf.append(b'{"term" : { "'+mytype+b'" : "'+myvalue+b'"}}')
                    outf+=b'{ "and" : ['+b', '.join(suboutf)+b']}'
                elif len(pathlist)==1:
                    [(mytype,myvalue)]=pathlist
                    outf+=b'{"term" : { "'+mytype+b'" : "'+myvalue+b'"}}'

                else:
                    atpic.log.debug(yy,'ignoring path....')

            else: # this a number (or fraction) or a range of number
                if mytype==b'f':
                    convertfct=atpic.aperture.f4elasticsearch
                elif mytype==b'speed':
                    convertfct=atpic.speed.speed4elasticsearch
                else:
                    convertfct=identity
                atpic.log.debug(yy,'this is a number or a range')
                pvalue=atpic.queryparser.parse_wordorrange(avalue)
                atpic.log.debug(yy,pvalue)
                if len(pvalue)==4:
                    atpic.log.debug(yy,'This is a range')
                    bracket_from=pvalue[0]
                    myvalue_from=pvalue[1]
                    myvalue_to=pvalue[2]
                    bracket_to=pvalue[3]
                    if bracket_from==b'[':
                        include_lower=b'true'
                    else:
                        include_lower=b'false'
                    if bracket_to==b']':
                        include_upper =b'true'
                    else:
                        include_upper=b'false'

                    # some fields are digitized:
                    myvalue_from=convertfct(myvalue_from)
                    myvalue_to=convertfct(myvalue_to)

                    # date field has several resolutions:
                    if atype in (b'date',b'blogsearch',b'blogpath',b'blog'):
                        atpic.log.debug(yy,'This is a date range')
                        (mytype,myvalue_from,myvalue_to)=atpic.dateutils.get_datefieldrangevalue(myvalue_from,myvalue_to,bracket_from,bracket_to)
                    outf+=b'{"range" : { "'+mytype+b'" : { "from": "'+myvalue_from+b'", "to" : "'+myvalue_to+b'", "include_lower" : "'+include_lower+b'", "include_upper" : "'+include_upper+b'" }}}'
                else:
                    atpic.log.debug(yy,'This is a number')
                    myvalue=pvalue[0]
                    myvalue=convertfct(myvalue)
                    # date field has several resolutions:
                    if atype in (b'date',b'blogsearch',b'blogpath',b'blog'):
                        atpic.log.debug(yy,'This is a number: date')
                        (mytype,myvalue)=atpic.dateutils.get_datefieldvalue(myvalue)
                        atpic.log.debug(yy,'This is a number: date with interpreted values',(mytype,myvalue))

                    if mytype!=b'': # can set set to zero lenght if all dates are asked
                        outf+=b'{"term" : { "'+mytype+b'" : "'+myvalue+b'"}}'


            if outf!=b'':
                # append to the relevant list
                if asign==b'-':
                    # outf+=b'}' # end of 'not'
                    outfm.append(outf)
                else:
                    outfp.append(outf)

    except:
        atpic.log.error(yy,traceback.format_exc())

    atpic.log.debug(yy,"output=",(outqp,outqm,outfp,outfm))
    return (outqp,outqm,outfp,outfm)


def add_coordinates_filter2(xmin,xmax,ymin,ymax,outqp,outqm,outfp,outfm):
    # this use our customer coord_ packed bits
    yy=atpic.log.setname(xx,'add_coordinates_filter2')
    atpic.log.debug(yy,"input=",(xmin,xmax,ymin,ymax,outqp,outqm,outfp,outfm))
    flist=[]
    (wlen,zonelist)=atpic.coordinates.get_filter_precision(xmin,ymin,xmax,ymax,b'4',b'16')
    for zone in zonelist:
        flist.append(b'{ "term" : { "coord_'+wlen+b'" : "'+zone+b'"}}')

    out=b', '.join(flist)
    out=b'{ "or" : ['+out+b']}'
    outfp.append(out)
    atpic.log.debug(yy,"output=",(outqp,outqm,outfp,outfm))
    return (outqp,outqm,outfp,outfm)

def add_coordinates_filter1(xmin,xmax,ymin,ymax,outqp,outqm,outfp,outfm):
    # this uses elasticsearch geo_bounding_box for locations
    yy=atpic.log.setname(xx,'add_coordinates_filter1')
    atpic.log.debug(yy,"input=",(xmin,xmax,ymin,ymax,outqp,outqm,outfp,outfm))
    flist=[]
    flist.append(b'{ "geo_bounding_box" : { "location" : {')
    flist.append(b'"top_left" : {')
    flist.append(b'"lat" : '+ymax)
    flist.append(b', "lon" : '+xmin)
    flist.append(b'},')
    flist.append(b'"bottom_right" : {')
    flist.append(b'"lat" : '+ymin)
    flist.append(b', "lon" : '+xmax)
    flist.append(b'}}}}')
    outfp.append(b' '.join(flist))
    atpic.log.debug(yy,"output=",(outqp,outqm,outfp,outfm))
    return (outqp,outqm,outfp,outfm)

def process_coordinates(parsed,outqp,outqm,outfp,outfm):
    #  we onlty accept '+' (include) no exclude
    # if more than one lat o lon, we choose one
    # if only one is set, then we take a default
    yy=atpic.log.setname(xx,'process_coordinates')
    atpic.log.debug(yy,"input=",(parsed,outqp,outqm,outfp,outfm))
    atpic.log.debug(yy,'parsed',parsed)
    lon=(b'+', b'lon', b'-179.99999999to180')
    lat=(b'+', b'lat', b'-90to90')
    found=False
    for (asign,atype,avalue) in parsed:
        if atype==b'lon':
            lon=(asign,atype,avalue)
            found=True
        elif atype==b'lat':
            lat=(asign,atype,avalue)
            found=True
    # at this stage we have our limits
    if found:
        plon=atpic.queryparser.parse_wordorrange(lon[2])
        plat=atpic.queryparser.parse_wordorrange(lat[2])
        atpic.log.debug(yy,'plon',plon)
        atpic.log.debug(yy,'plat',plat)
        if len(plon)==4:
            xmin=plon[1]
            xmax=plon[2]
        if len(plat)==4:
            ymin=plat[1]
            ymax=plat[2]
        # (outqp,outqm,outfp,outfm)=add_coordinates_filter1(xmin,xmax,ymin,ymax,outqp,outqm,outfp,outfm)
        (outqp,outqm,outfp,outfm)=add_coordinates_filter2(xmin,xmax,ymin,ymax,outqp,outqm,outfp,outfm)



    atpic.log.debug(yy,"output=",(outqp,outqm,outfp,outfm))
    return (outqp,outqm,outfp,outfm)




def parsed2json(parsed,aid,afrom,size):
    # aid= authenticated user id, b'' if not authenticated
    yy=atpic.log.setname(xx,'parsed2json')
    atpic.log.debug(yy,"input=",(parsed,aid,afrom,size))
    ajson=b''

    outqp=[] # out query +
    outqm=[] # out query -

    outfp=[] # out filter +
    outfm=[] # out filter -



    # main loop:

    for (asign,atype,avalue) in parsed:
        (outqp,outqm,outfp,outfm)=process_one_condition(asign,atype,avalue,outqp,outqm,outfp,outfm)

    # process coordinates (lat, lon) which were ignored above
    (outqp,outqm,outfp,outfm)=process_coordinates(parsed,outqp,outqm,outfp,outfm)
    # append the permissions
    permissions=forge_permission_filter(aid)
    outfp.append(permissions)


    atpic.log.debug(yy,'outqp',outqp)
    atpic.log.debug(yy,'outqm',outqm)
    atpic.log.debug(yy,'outfp',outfp)
    atpic.log.debug(yy,'outfm',outfm)
    atpic.log.debug(yy,'+++++++')

    # a this stage should be able to forge the json only with outqp, ouqm and outfl

    #  set the "query"
    outl=[]
    if len(outqp)==0 and len(outqm)==0:
        outl.append(b'"query" : {"match_all" : {}}')
    else:
        outl.append(b'"query" : { "bool" : { "must": ['+b', '.join(outqp)+b'], "must_not" : ['+b', '.join(outqm)+b']}}')

    # set the "size"
    outl.append(b'"size" : '+size)
    if afrom!=b'':
        outl.append(b'"from" : '+afrom)

    # set the fields
    outl.append(b'"fields" : '+get_fields())

    # set the "sort"
    asort=set_sort(parsed)
    atpic.log.debug(yy,'asort',asort)
    if asort!=b'':
        outl.append(asort)
                
    # set the "filter"
    if len(outfp)==1 and len(outfp)==0:
        outl.append(b'"filter" : '+b', '.join(outfp)+b'')
    else:
        # general case:
        # build a new list of negations:
        outfmm=[]
        for condn in outfm:
            outfmm.append(b'{ "not" : "'+condn+b' }')
        outl.append(b'"filter" : { "and" : ['+b', '.join(outfp+outfmm)+b']}')

    ajson=b'{ '+b', '.join(outl)+b'}'

    atpic.log.debug(yy,"output=",ajson)
    return ajson


def search_uid(parsed):
    # take the first +uid: to be used for routing
    yy=atpic.log.setname(xx,'search_uid')
    atpic.log.debug(yy,"input=",(parsed))
    uid=b''
    for ele in parsed:
        (asign,atype,avalue)=ele
        if asign==b'+' and atype==b'uid':
            uid=avalue
    atpic.log.debug(yy,"output=",uid)
    return uid

def query2json(query,aid,afrom,size):
    yy=atpic.log.setname(xx,'query2json')
    atpic.log.debug(yy,"input=",(query,aid,afrom,size))
    parsed=atpic.queryparser.parse_first(query)
    ajson=parsed2json(parsed,aid,afrom,size)
    atpic.log.debug(yy,"output=",(parsed,ajson))
    return (parsed,ajson)

def send_msearch(essock,ajson):
    yy=atpic.log.setname(xx,'send_msearch')
    atpic.log.debug(yy,"input=",ajson)
    uri=b'/atpic/pic/_msearch' #+routing # ?routing='+uid.decode('utf8')
    content=atpic.zmq_elastic_client.http_general(essock,b'GET',uri,ajson)
    t1b=time.time()
    atpic.log.debug(yy,'content',content)
    t2b=time.time()
    atpic.log.debug(yy,'took',t2b-t1b)
    atpic.log.debug(yy,"output=",content)
    return content

def send_query(essock,query,afrom,size,uid,aid):
    # uid= the user site id to use routing, b'' if atpic-wide search
    # aid= authenticated user id, b'' if not authenticated
    yy=atpic.log.setname(xx,'send_query')
    atpic.log.debug(yy,"input=",(query,afrom,size,uid,aid))
    if size==b'':
        size=b'10'
    (parsed,ajson)=query2json(query,aid,afrom,size)
    if uid==b'':
        uid2=search_uid(parsed)
        if uid2!=b'':
            uid=uid2
    t1a=time.time()
    if uid!=b'':
        routing=b'?routing='+uid
    else:
        routing=b''
    uri=b'/atpic/pic/_search'+routing # ?routing='+uid.decode('utf8')
    content=atpic.zmq_elastic_client.http_general(essock,b'GET',uri,ajson)
    t1b=time.time()
    atpic.log.debug(yy,"output=",content)
    return content

# ============================================================
#
#   2) specialized query parser for FACETS
# 
# ============================================================
# we have thre factes:
# date, geo, path (and vpath)

# ====================
#    forge queries
# ====================

# common:

def multi_header(uid):
    # the header in a multi search 
    yy=atpic.log.setname(xx,'multi_header')
    atpic.log.debug(yy,"input=",uid)
    if uid!=b'':
        header=b'{ "index" : "atpic", "type" : "pic", "routing": "'+uid+b'"}'
    else:
        header=b'{ "index" : "atpic", "type" : "pic"}'
    atpic.log.debug(yy,"output=",header)
    return header


# --------------------------------------------
#         date
# --------------------------------------------
def get_facet_date_list(datestring):
    # returns  a list of dates
    # datestring can be /200 /2005 /2005/12
    yy=atpic.log.setname(xx,'get_facet_date_list')
    atpic.log.debug(yy,"input=",(datestring))
    cleaneddate=atpic.dateutils.remove_nondigits(datestring)
    atpic.log.debug(yy,"cleaneddate=",(cleaneddate))
    alen=len(cleaneddate)
    alist=[]
    if alen<4: # TO BE IMPROVED! using tens and hundreds of years
        # take the last 20 years
        today=datetime.date.today()
        year=today.year
        atpic.log.debug(yy,"today's year=",year)
        for i in range(year-19,year+1): # go back 20 years
            dateto=atpic.mybytes.int2bytes(i)
            dateto=dateto.rjust(4,b'0')
            alist.append(dateto)

    elif alen==4:
        for i in range(1,13): # there are 12 months
            dateto=atpic.mybytes.int2bytes(i)
            dateto=dateto.rjust(2,b'0')
            alist.append(cleaneddate+dateto)
    
    elif alen==6:
        year=atpic.mybytes.bytes2int(cleaneddate[0:4])
        month=atpic.mybytes.bytes2int(cleaneddate[4:6])
        (startday,endday)=calendar.monthrange(year, month)
        for i in range(1,endday+1): # there are 31 days maxi in one month
            dateto=atpic.mybytes.int2bytes(i)
            dateto=dateto.rjust(2,b'0')
            alist.append(cleaneddate+dateto)
    
    atpic.log.debug(yy,"output=",alist)
    return alist

def forge_facet_date_search(alist,uid,aid):
    # unit test this:
    yy=atpic.log.setname(xx,'forge_facet_date_search')
    atpic.log.debug(yy,"input=",(alist,uid,aid))
    # we do a multi search
    header=multi_header(uid)
    ajs=[]
    # the query:
    for ymd in alist:
        ajs.append(header)
        # we forge a query:
        query=b'date:'+ymd+b' uid:'+uid
        size=b'1'
        afrom=b'0'
        (parsed,queryjson)=query2json(query,aid,afrom,size)
        ajs.append(queryjson)
    ajson=b'\n'.join(ajs)+b'\n'
    atpic.log.debug(yy,"output=",ajson)
    return ajson


# --------------------------------------------
#         path
# --------------------------------------------
def get_facet_path_list_list(essock,uid,path,pathtype):
    # used for a path or vpath first search
    #  we convert the json result to a simpler python list
    yy=atpic.log.setname(xx,'get_facet_path_list_list')
    atpic.log.debug(yy,'input',(uid,path,pathtype))

    json=get_facet_path_list(essock,uid,path,pathtype)
    jsonpy=atpic.jsonat_json2python.parse(json)
    atpic.log.debug(yy,jsonpy)
    hlist=jsonpy[b'hits'][b'hits']
    resl=[]
    for ahit in hlist:
        path=ahit[b'fields'][b'path'][0] # new elasticsearch
        resl.append(path)
    atpic.log.debug(yy,"output=",resl)
    return resl

def get_facet_path_list(essock,uid,path,pathtype):
    if pathtype==b'tree':
        pathtype=b'path'
    if pathtype==b'vtree':
        pathtype=b'vpath'
    size=b'100' # maximum number of direct folder children of a folder
    yy=atpic.log.setname(xx,'get_facet_path_list')
    atpic.log.debug(yy,'input',(uid,path,pathtype))
    ajson=b'{ "size": '+size+b', "query" : { "match_all" : {}}, "fields" : ["parent","path"], "filter" : { "and" : [{"term" : {"parent" : "'+path+b'"}}, { "term" : {"uid" : "'+uid+b'"}}]}}'
    t1a=time.time()
    if uid!=b'':
        routing=b'?routing='+uid
    else:
        routing=b''
    uri=b'/atpic/'+pathtype+b'/_search'+routing # ?routing='+uid.decode('utf8')
    content=atpic.zmq_elastic_client.http_general(essock,b'GET',uri,ajson)
    t1b=time.time()
    atpic.log.debug(yy,content)
    atpic.log.debug(yy,'output',content)
    
    return content

def forge_atpicquery_below(pathtype,path,uid):
    yy=atpic.log.setname(xx,'forge_atpicquery_below')
    atpic.log.debug(yy,'input',pathtype,path,uid)
    if path==None:
        path=b''
    path=path.strip(b'/')
    if path!=b'':
        path=b'/'+path
    query=pathtype+b':'+path+b'/* uid:'+uid
    atpic.log.debug(yy,'output searchquery',query)
    return query

def forge_facet_path_list_search(uid,pathlist,aid,pathtype):
    # path type can be: b'path' or b'vpath'
    # it is not a big problem if there is more path in pathlist than necessary
    # they will just give a zero match
    # unit test this:
    yy=atpic.log.setname(xx,'forge_facet_path_list_search')
    atpic.log.debug(yy,'input',(uid,pathlist,aid,pathtype))
    # we do a multi search
    header=multi_header(uid)
    ajs=[]
    # the query:
    for apath in pathlist:
        ajs.append(header)
        # we forge a query:
        query=forge_atpicquery_below(pathtype,apath,uid)
        atpic.log.debug(yy,"searchquery",query)
        size=b'1'
        afrom=b'0'
        (parsed,queryjson)=query2json(query,aid,afrom,size)
        ajs.append(queryjson)
    ajson=b'\n'.join(ajs)+b'\n'
    atpic.log.debug(yy,"output=",ajson)
    return ajson



# --------------------------------------------
#         geo (coord)
# --------------------------------------------
def geopath2bounds(path):
    (empty,xmin,xmax,ymin,ymax)=path.split(b'/')
    xmin=atpic.mybytes.bytes2float(xmin)
    xmax=atpic.mybytes.bytes2float(xmax)
    ymin=atpic.mybytes.bytes2float(ymin)
    ymax=atpic.mybytes.bytes2float(ymax)
    return (xmin,xmax,ymin,ymax)

def get_facet_geo_list(path):
    # geopath
    yy=atpic.log.setname(xx,'get_facet_geo_list')
    atpic.log.debug(yy,"input=",path)
    if path==b'/':
        path=b'/-180.0/180.0/-90.0/90.0'
        atpic.log.debug(yy,"newpath=",path)
    (xmin,xmax,ymin,ymax)=geopath2bounds(path)
    facet=atpic.coordinates.get_facets(xmin,xmax,ymin,ymax)
    atpic.log.debug(yy,"output=",facet)
    return facet

def forge_facet_geo_search(pathlist,uid,aid):
    yy=atpic.log.setname(xx,'forge_facet_geo_search')
    # we expect an exact pathlist, i.e a pathlist that correspond to 1 facet only
    atpic.log.debug(yy,"input=",(pathlist,uid,aid))
    # we do a multi search
    header=multi_header(uid)
    ajs=[]
    # the query:
    for apath in pathlist:
        ajs.append(header)
        # we forge a query:
        query=b'geopathexact:'+apath+b' uid:'+uid
        size=b'1'
        afrom=b'0'
        (parsed,queryjson)=query2json(query,aid,afrom,size)
        ajs.append(queryjson)
    ajson=b'\n'.join(ajs)+b'\n'
    atpic.log.debug(yy,"output=",ajson)
    return ajson
    return ajson

def forge_facet_coord_search(uid,aid,xmin,xmax,ymin,ymax):
    # use packed fields
    yy=atpic.log.setname(xx,'forge_facet_coord_search2')
    atpic.log.debug(yy,"input=",(uid,aid,xmin,xmax,ymin,ymax))
    (wlen,zonelist)=atpic.coordinates.get_filter_precision(xmin,ymin,xmax,ymax,b'7',b'64')
    ajson=forge_facet_coord_list_search(uid,aid,xmin,xmax,ymin,ymax,wlen,zonelist)
    return ajson

def forge_facet_coord_list_search(uid,aid,xmin,xmax,ymin,ymax,wlen,zonelist):
    yy=atpic.log.setname(xx,'forge_facet_coord_list_search')
    header=multi_header(uid)
    ajs=[]
    for zone in zonelist:
        ajs.append(header)
        query=b'packedcoord:'+zone+b'.'+wlen   
        size=b'1'
        afrom=b'0'
        (parsed,queryjson)=query2json(query,aid,afrom,size)
        ajs.append(queryjson)
    ajson=b'\n'.join(ajs)+b'\n'
    atpic.log.debug(yy,"output=",ajson)
    return ajson

if __name__ == "__main__":
    aid=b'1'
    uid=b'1'
    print("testing elasticsearch")
    """
    facet_geo()
    # test1()
    # facet_directory(b'1',b'/italia2006',b'1')
    # facet_date(b'1',b'',b'',b'',b'1')
    # send_query(b'+uid:1', b'1', b'1',uid,aid)
    send_query(b'+uid:1', b'', b'',uid,aid)
    send_query(b'firenze +uid:1', b'', b'',uid,aid)
    send_query(b'+f:5.6', b'', b'',uid,aid)
    send_query(b'+speed:1/500', b'', b'',uid,aid)
    send_query(b'+speed:1/500to1/125', b'', b'',uid,aid)
    send_query(b'-speed:1/500', b'', b'',uid,aid)
    send_query(b'+make:canon', b'', b'',uid,aid)
    send_query(b'+model:"canon powershot"', b'', b'',uid,aid)
    send_query(b'+make:canon -model:powershot', b'', b'',uid,aid)
    send_query(b'italia2006', b'', b'',uid,aid)
    send_query(b'test_exif_geo.jpg', b'', b'',uid,aid)
    # send_query(b'+originalname:test_exif_geo.jpg', b'', b'',uid,aid)
    send_query(b'+date:2008', b'', b'',uid,aid)
    # send_query(b'+datetime:2008', b'', b'',uid,aid)
    send_query(b'+filetype:jpg', b'', b'',uid,aid)
    send_query(b'+dns:alex', b'', b'',uid,aid)
    send_query(b'+gid:1', b'', b'',uid,aid)
    send_query(b'+pid:291606', b'', b'',uid,aid)
    send_query(b'+filename:test_exif_geo.jpg', b'', b'',uid,aid)
    send_query(b'+uid:1', b'', b'',uid,aid)
    send_query(b'+uid:1 +sort:random', b'', b'',uid,aid)
    send_query(b'+uid:1 +sort:date', b'', b'',uid,aid)
    send_query(b'+uid:1 +date:2004', b'', b'',uid,aid)
    send_query(b'+uid:1 +date:2004to2010', b'', b'',uid,aid)
    send_query(b'+uid:1 +date:2008,', b'', b'',uid,aid)
    send_query(b'+tree:/nathalie', b'', b'',uid,aid)
    send_query(b'-tree:/nathalie', b'', b'',uid,aid)
    send_query(b'-tree:alex/nathalie', b'', b'',uid,aid)
    send_query(b'+tree:alex/nathalie', b'', b'',uid,aid)
    send_query(b'+vtree:alex/alex', b'', b'',uid,aid)
    send_query(b'+vtree:alex/alex/* +uid:1', b'', b'',uid,aid)
    #  coord
    send_query(b'lat:40to50 lon:0to20', b'', b'',uid,aid)
    # try: except:
    send_query(b'+speed:1/500/400', b'', b'',uid,aid)
    """
    # send_query(b'lat:40to50 lon:0to20', b'', b'',uid,aid)

    # 
    # send_query(b'+tree:alex/nathalie', b'', b'',uid,aid)
    # send_query(b'+tree:/nathalie', b'', b'',uid,aid)
    # send_query(b'+vtree:alex/alex', b'', b'',uid,aid)
    # send_query(b'+vtree:alex/alex/* +uid:1', b'', b'',uid,aid)
    # send_query(b'+uid:1 +sort:random', b'', b'',uid,aid)
    # send_query(b'+uid:1 +sort:random lat:-90to90 lon:-179to180', b'', b'',uid,aid)
    # send_query(b'+uid:1 lon:0to20 lat:40to50', b'', b'',uid,aid)

    """
    uid=b'1'
    year=b''
    month=b''
    day=b''
    aid=b''
    ajson=forge_facet_date_search(uid,year,month,day,aid)
    send_msearch(ajson)
    pathlist=[b'italia2006',b'nikond40']
    pathtype=b'tree'
    ajson=forge_facet_path_list_search(uid,pathlist,aid,pathtype)    
    send_msearch(ajson)
    xmin=b'0'
    xmax=b'20'
    ymin=b'30'
    ymax=b'50'
    ajson=forge_facet_coord_search(uid,aid,xmin,xmax,ymin,ymax)
    send_msearch(ajson)
    """
    
    """
    uid=b'1'
    # path=b'italia2006'
    path=b''
    pathtype=b'tree' # b'gallery'
    resl=get_facet_path_list_list(uid,path,pathtype)
    print(resl)
    """


    # send_query(b'+uid:1 +sort:random lat:-90to90 lon:-179to180', b'', b'',uid,aid)
    # send_query(b'+uid:1 +sort:random', b'', b'',uid,aid)
    # send_query(b'+uid:1', b'', b'',uid,aid)
    # send_query(b'+pid:291607', b'', b'',uid,aid)
    # send_query(b'italia2006', b'', b'',uid,aid)

    # send_query(b'+uid:1 +geopackpath:/4/1/9', b'', b'',uid,aid)
    # send_query(b'+uid:1 +geopath:/-180/-90/180/90', b'', b'',uid,aid)
    send_query(b'+uid:1 +geopathexact:/-180/180/-90/90', b'', b'',uid,aid)
    #  send_query(b'+sort:random', b'', b'',uid,aid)
