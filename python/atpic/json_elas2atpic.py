#!/usr/bin/python3
import atpic.jsonat_json2python
import atpic.mybytes
import atpic.autorize

# should we store all the storedates in the index?
# or do a SQL request by UID,PID
# note: some fields are only in the index like popularity
# latitude and longitute are CASCADED

# need a index update at each new storedate
# need to forge the encrypted URL
# but we know we need exif in the index as we allow search by aperture, speed, make

# two functions:
# one for facets
# one for search

xx=atpic.log.setmod("DEBUG","json_elas2atpic")


def display_onefield(fields,key):
    """
    This is a clever function:
    older versions of elasticsearch used to return single values, now it always return arrays

    http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/_return_values.html
    
    Field values, in response to the fields parameter, are now always returned as arrays. A field could have single or multiple values, which meant that sometimes they were returned as scalars and sometimes as arrays. By always returning arrays, this simplifies user code. The only exception to this rule is when fields is used to retrieve metadata like the routing value, which are always singular. Metadata fields are always returned as scalars. 
    
    """
    aval=fields.get(key,None)
    if aval:
        if type(aval) is bytes:
            pass
        elif type(aval) is list:
            aval=aval[0]
    return aval

def display_onepic(fields,aid,rank,docompo,compolist,environ):
    # display ahit fields
    yy=atpic.log.setname(xx,'display_onepic')
    atpic.log.debug(yy,'input=',(fields,aid,rank,docompo,compolist,environ))

    xmll=[]
    mode=display_onefield(fields,b'mode')
    uid=display_onefield(fields,b'uid')
    autori=atpic.autorize.authorization_elasticsearch(mode,uid,aid)

    pid=display_onefield(fields,b'pid')
    uid=display_onefield(fields,b'uid')
    gid=display_onefield(fields,b'gid')
    servershort=display_onefield(fields,b'servershort')

    xmll.append(b'<pic>')
    xmll.append(b'<rank>')
    xmll.append(atpic.mybytes.int2bytes(rank))
    xmll.append(b'</rank>')
    xmll.append(b'<pid>')
    xmll.append(pid)
    xmll.append(b'</pid>')
    xmll.append(b'<uid>')
    xmll.append(uid)
    xmll.append(b'</uid>')
    xmll.append(b'<gid>')
    xmll.append(gid)
    xmll.append(b'</gid>')
    xmll.append(b'<servershort>')
    xmll.append(servershort)
    xmll.append(b'</servershort>')

    width=display_onefield(fields,b'width')
    height=display_onefield(fields,b'height')


    #  now we need to present the md5 hashes depending on autorization
    for reso in [b'r70',b'r160',b'r350',b'r600',b'r1024',]:
        pathstore=display_onefield(fields,b'pathstore_'+reso)
        if pathstore:
            xmll.append(b'<pathstore_'+reso+b'>')
            xmll.append(pathstore)
            xmll.append(b'</pathstore_'+reso+b'>')
    atpic.log.debug(yy,'now doing width, height')
    if width and height:
        xmll.append(b'<width>')
        xmll.append(width)
        xmll.append(b'</width>')
        xmll.append(b'<height>')
        xmll.append(height)
        xmll.append(b'</height>')


        widthi=atpic.mybytes.bytes2int(width)
        heighti=atpic.mybytes.bytes2int(height)
        atpic.log.debug(yy,'(widthi,heighti)=',(widthi,heighti))
        ratio=min(widthi,heighti)/max(widthi,heighti)
        for reso in [b'70',b'160',b'350',b'600',b'1024',]:
            resoi=atpic.mybytes.bytes2int(reso)
            mini=atpic.mybytes.int2bytes(int(resoi*ratio))
            if widthi>heighti:
                swidth=reso
                sheight=mini
            else:
                swidth=mini
                sheight=reso
            xmll.append(b'<width_r'+reso+b'>')
            xmll.append(swidth)
            xmll.append(b'</width_r'+reso+b'>')
            xmll.append(b'<height_r'+reso+b'>')
            xmll.append(sheight)
            xmll.append(b'</height_r'+reso+b'>')


    xmll.append(b'</pic>')

    if docompo:
        compolist.append(b'http://'+servershort+b'.atpic.com/gallery/'+gid+b'/pic/'+pid)

    # print("xmll=",xmll)
    print('hi')
    xml=b''.join(xmll)
    atpic.log.debug(yy,'output=',(xml,compolist))
    return (xml,compolist)

def display_facets(facet_list,json,aid):
    # facet_list is a list of bytes
    # json is the result of msearch
    yy=atpic.log.setname(xx,'display_facets')
    atpic.log.debug(yy,"input=",(facet_list,json,aid))
    jsonob=atpic.jsonat_json2python.parse(json)
    atpic.log.debug(yy,jsonob[b'responses'])
    response_list=jsonob[b'responses']
    xmll=[]
    xmll.append(b'<Facet>')
    for (facet,response) in zip(facet_list,response_list):
        atpic.log.debug(yy,facet,response)
        xmll.append(b'<facet>')
        xmll.append(b'<name>')
        xmll.append(facet)
        xmll.append(b'</name>')
        xmll.append(b'<hits>')
        total=response[b'hits'][b'total']
        xmll.append(total)
        xmll.append(b'</hits>')
        if total!=b'0':
            fields=response[b'hits'][b'hits'][0][b'fields']
            docompo=False
            (xmlout,compolist)=display_onepic(fields,aid,1,docompo,[],{}) # dummy rank
            xmll.append(xmlout)
        xmll.append(b'</facet>')
    xmll.append(b'</Facet>')
    xml=b''.join(xmll)

    atpic.log.debug(yy,'output',xml)

    return xml



def display(json,afrom,size,rank,aid,compolist,environ):
    yy=atpic.log.setname(xx,'display')
    atpic.log.debug(yy,"input=",(json,afrom,size,rank,aid,compolist))
    xmlobj=atpic.jsonat_json2python.parse(json)
    atpic.log.debug(yy,'xmlobj.took',xmlobj[b'took'])
    hits_total=xmlobj[b'hits'][b'total']
    hits_totalb=atpic.mybytes.bytes2int(hits_total)

    atpic.log.debug(yy,'xmlobj.hits.total',hits_total)
    xmll=[]
    afromi=atpic.mybytes.bytes2int(afrom)
    docompo=False
    if rank:
        docompo=True
    if hits_totalb>0:
        if not rank:
            rank=afromi+1
        else:
            rank=atpic.mybytes.bytes2int(rank)
        atpic.log.debug(yy,'new rank (init)',rank)
        for ahit in xmlobj[b'hits'][b'hits']:
            atpic.log.debug(yy,ahit[b'fields'])
            fields=ahit[b'fields']
            (xmlout,compolist)=display_onepic(fields,aid,rank,docompo,compolist,environ)
            xmll.append(xmlout)
            rank=rank+1
    xml=b''.join(xmll)
    atpic.log.debug(yy,'output',(xml,compolist))
    return (hits_total,xml,compolist)


if __name__=="__main__":
    print('hi')
