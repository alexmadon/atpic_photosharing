#!/usr/bin/python3

# apt-get install python3-docutils
# use python reStructuredText format

# atpic_role is a custom role
import re
import io

import docutils.io
import docutils.nodes
import docutils.parsers.rst.roles
import docutils.core

from lxml import etree
import traceback

import atpic.errors
import atpic.forgesql
import atpic.hashat
import atpic.libpqalex
import atpic.log
import atpic.mybytes
import atpic.parameters
import atpic.wiki_section
import atpic.wikiparser
import atpic.xplo
xx=atpic.log.setmod("INFO","wiki_rst")

# http://connect.ed-diamond.com/GNU-Linux-Magazine/GLMF-104/Grokking-Docutils-et-reStructuredText
# http://pastebin.com/isRzAatW
# #112  -> http://mytracsite/tickets/112
# r1023 -> http://mytracsite/changeset/1023
 
# edit sections alawikipedia/mediawiki
# http://www.arnebrodowski.de/blog/write-your-own-restructuredtext-writer.html



def parse_key(key):
    yy=atpic.log.setname(xx,'parse_key')
    atpic.log.debug(yy,'input=',key)
    # need to sanitize the <
    # parse with grammar or regex?
    key_array=atpic.wikiparser.parse2array(key)
    atpic.log.debug(yy,'output=',key_array)
    return key_array


def transform_ref(references):
    """
    input: an array with keys and True values, e.g. {'p:123': True, 'hello': True}
    output: a new array with same keys, but values are parsed keys e.g:
       {'hello': {'wikipage': 'hello'}, 'p:123': {'image': '123'}
    """
    yy=atpic.log.setname(xx,'transform_ref')
    atpic.log.debug(yy,'input=',references)
    new_references={}
    for key in references.keys():
        atpic.log.debug(yy,'key=',key)
        res=parse_key(key)
        new_references[key]=res
    atpic.log.debug(yy,'ouput=',new_references)
    return new_references



def uid2partition(uid,db):
    yy=atpic.log.setname(xx,'uid2partition')
    atpic.log.debug(yy,'input=',(uid,db))
    if uid==b'':
        uid=b'1'
    try:
        query=b"select _user._partition,_user._servershort from _user where _user.id=$1 and _deleted=0"
        values=[uid,]
        # a prepared statement
        statement=b''
        result1=atpic.libpqalex.pq_prepare(db,statement,query)
        result=atpic.libpqalex.pq_exec_prepared(db,statement,values)
        result=atpic.libpqalex.process_result(result)
        atpic.log.debug(yy,'result',result)
        partition=result[0][b"_partition"]
        servershort=result[0][b"_servershort"]
    except:
        raise atpic.errors.Error404(b'Could not find user with uid',uid)
    atpic.log.debug(yy,'output=',(partition,servershort))
    return (partition,servershort)



def transform_refsql(db,references,hxplo,pxplo,aid,uid,environ):
    """
    references: an array of array {key:{type:value,},}
    """
    # forge the sql request depending on the value
    # execute SQL
    # exploit result to create new html nodes, store then as a new array
    # could block process similar sql requests
    # using SELECT ... WHERE ... IN ($1,$2,...)
    # group wikipages, pics, etc...


    # forge an atpicdata.com pic link
    # partition and servershort could get retrieved only once
    # hashvalue=atpic.hashat.forge_pathstorehash(pid,resolutioncode,pathondisk,partition,extension)

    yy=atpic.log.setname(xx,'transform_refsql')
    atpic.log.debug(yy,'input=',(db,references,hxplo.list(),pxplo.list(),aid,uid))
    new_references={}



    (partition,servershort)=uid2partition(uid,db)
    # cleaner code and more flexible:
    # just parse several times

    image_counter=0 
    image_max=20 # prohibit having too many images per wiki page

    dotcom=atpic.parameters.get_tld(environ) # get dotcom

    for key in references.keys():
        atpic.log.debug(yy,'key=',key)
        karray=references[key]
        if 'image' in karray.keys():
            atpic.log.debug(yy,'this is an image, we need SQL')
            try:
                image_counter=image_counter+1
                pid=atpic.mybytes.int2bytes(int(karray['image']))
                if 'resolution' in  karray.keys():
                    resolutioncode=karray['resolution'].encode('utf8')
                else:
                    resolutioncode=b'r600' # default value for resolution
                (query,query_args)=atpic.forgesql.forge_wikiimage(uid,pid,resolutioncode)
                # a prepared statement
                statement=b''
                result1=atpic.libpqalex.pq_prepare(db,statement,query)
                result=atpic.libpqalex.pq_exec_prepared(db,statement,query_args)
                result=atpic.libpqalex.process_result(result)
                pathondisk=result[0][b"_pathstore"]        
                extension=result[0][b"_extension"]        
                gid=result[0][b"_gallery"]        
                hashvalue=atpic.hashat.forge_pathstorehash(pid,resolutioncode,pathondisk,partition,extension)


                picurl=b'http://'+servershort+b'.atpicdata'+dotcom+b'/'+hashvalue
                karray['url']=picurl.decode('utf8')
                # link to more details
                piclink=b'http://'+servershort+b'.atpic'+dotcom+b'/gallery/'+gid+b'/pic/'+karray['image'].encode('utf8')
                karray['link']=piclink.decode('utf8')
            except:
                karray['error']='could not find picture with key '+key
                atpic.log.error(yy,traceback.format_exc())

            new_references[key]=karray
    
        elif 'wikipage' in karray.keys():
            atpic.log.debug(yy,'this is a wikipage')
            new_references[key]=karray
        elif 'internal' in karray.keys():
            atpic.log.debug(yy,'this is an internal')
            new_references[key]=karray
        elif 'user' in karray.keys():
            atpic.log.debug(yy,'this is a user')
            new_references[key]=karray
        elif 'userdns' in karray.keys():
            atpic.log.debug(yy,'this is a userdns')
            new_references[key]=karray
        elif 'gallery' in karray.keys():
            atpic.log.debug(yy,'this is a gallery')
            new_references[key]=karray

    atpic.log.debug(yy,'output=',new_references)
    return new_references




def transform_refnodes(references):
    # returns an array that can be used directly by the atpic_role
    # CAN BE UNIT TESTED
    # we return an array of doublets almost like a role
    # except that errors are just list of strings
    """
    http://docutils.sourceforge.net/docutils/parsers/rst/roles.py
    Interpreted role functions return a tuple of two values:
    
    - A list of nodes which will be inserted into the document tree at the
    point where the interpreted role was encountered (can be an empty
    list).
    
    - A list of system messages, which will be inserted into the document tree
    immediately after the end of the current inline block (can also be empty).
    
    """
    """
    myuri='http://mysite.com/'+text+'||'+rawtext
    reference = docutils.nodes.reference(rawtext, text,refuri=myuri,classes=['piclink',])
    
    image = docutils.nodes.image(uri="somr_uri.png", target="mytarget",alt="somealt",classes=["piclink",])
    
    # http://osdir.com/ml/text.docutils.devel/2008-02/msg00021.html
    # https://docs.python.org/3/library/operator.html
    
    # operator.iadd(a, b)
    # operator.__iadd__(a, b)
    #  a = iadd(a, b) is equivalent to a += b.
    # http://docutils.sourceforge.net/docutils/nodes.py
    reference+=image # put the image in the reference <a/>
    
    atpic.log.debug(yy,'as we are in 2nd pass, we create nodes')
    return ([reference,image], [])
    """
    yy=atpic.log.setname(xx,'transform_refnodes')
    atpic.log.debug(yy,'input=',references)
    new_references={}
    for key in references.keys():
        atpic.log.debug(yy,'key=',key)
        karray=references[key]
        if 'image' in karray.keys():
            atpic.log.debug(yy,'this is an image')
            if 'error' in karray.keys():
                new_references[key]=([],[karray['error']])

                # new_references[key]=([problem],[])
            else:
                
                reference = docutils.nodes.reference('', '',refuri=karray['link'],classes=['piclink',],internal=True)
                
                image = docutils.nodes.image(uri=karray['url'], target="mytarget",alt="somealt",classes=["piclink",])
    
                # http://osdir.com/ml/text.docutils.devel/2008-02/msg00021.html
                # https://docs.python.org/3/library/operator.html
                
                # operator.iadd(a, b)
                # operator.__iadd__(a, b)
                #  a = iadd(a, b) is equivalent to a += b.
                # http://docutils.sourceforge.net/docutils/nodes.py
                reference+=image # put the image in the reference <a/>
                
                atpic.log.debug(yy,'as we are in 2nd pass, we create nodes')
                
                new_references[key]=([reference,], [])
                # new_references[key]=([], [])
                
        elif 'wikipage' in karray.keys():
            atpic.log.debug(yy,'this is a wikipage')
            alink='/wiki/'+karray['wikipage']
            if 'link' in karray.keys():
                atext=karray['link']
            else:
                atext=karray['wikipage']
            reference = docutils.nodes.reference(atext, atext,refuri=alink,classes=['wikilink',],internal=True)
            new_references[key]=([reference,],[])
        elif 'internal' in karray.keys():
            atpic.log.debug(yy,'this is an internal')
            atext=karray['wikipage']
            if 'link' in karray.keys():
                alink=karray['link']
            else:
                alink=atext
            reference = docutils.nodes.reference(atext, atext,refuri=alink,classes=['internallink',],internal=True)
            new_references[key]=([reference,],[])
        elif 'user' in karray.keys():
            atpic.log.debug(yy,'this is a user')
            new_references[key]=([],[])
        elif 'userdns' in karray.keys():
            atpic.log.debug(yy,'this is a userdns')
            new_references[key]=([],[])
        elif 'gallery' in karray.keys():
            atpic.log.debug(yy,'this is a gallery')
            new_references[key]=([],[])
        else:
            atpic.log.debug(yy,'this is unkown')
            new_references[key]=([],['UNKNOWN'])
    atpic.log.debug(yy,'output=',new_references)
    return new_references



# security related settings used by Trac are to turn off include and raw
# http://pydoc.net/Python/Trac/0.12.1/trac.mimeview.rst/
# http://docutils.sourceforge.net/docs/howto/security.html







# NEWWWWWWW

def doparse(text,mysettings):
    # input: wiktext to convert + settings
    # output: html text + settings
    yy=atpic.log.setname(xx,'doparse')
    atpic.log.debug(yy,'input=',(text,mysettings))


    # use publish_programmatically as we need access to publisher settings

    (output, pub) = docutils.core.publish_programmatically(
        source=text, # the input
        source_path=None, 
        source_class=docutils.io.StringInput,
        destination_class=docutils.io.StringOutput,
        destination=None,
        destination_path=None,
        reader=None, reader_name='standalone',
        parser=None, parser_name='restructuredtext',
        writer=atpic.wiki_section.MyHTMLWriter(),writer_name=None, # custom Writer (sections)
        settings=None, 
        settings_spec=None,
        settings_overrides=mysettings, # custom security settings + environment
        config_section=None,
        enable_exit_status=False)

    # print('dirparts',pub.writer.parts)
    # print('dirpub',dir(pub))
    # print('dirpub.settings',pub.settings)
    # text=parts['html_body'].encode('utf8')
    # atpic.log.debug(yy,'output=',(text))
    # print(mysettings)
    result=(pub.writer.parts['html_body'].encode('utf8'),pub.settings.__dict__)
    atpic.log.debug(yy,'output=',result)

    # print('pub.settings',pub.settings)
    # print('dirpub.settings',dir(pub.settings))
    return result





def get_needwikihtml(hxplo,pxplo):
    # can be unit tested
    yy=atpic.log.setname(xx,'get_needwikihtml')
    atpic.log.debug(yy,'input=',(hxplo.list(),pxplo.list()))
    needwikihtml=False
    if pxplo.keys()==[b'wiki']:
        needwikihtml=True
    elif pxplo.keys()==[b'wiki',b'revision']:
        atpic.log.debug(yy,'wiki,revision')
        revs=pxplo.getmatrix(1,1)
        atpic.log.debug(yy,'revs=',revs)
        if revs:
            pattern=re.compile(b'^([0-9]+)$')
            b=pattern.match(revs)
            if b:
                needwikihtml=True
    atpic.log.debug(yy,'output=',needwikihtml)
    return needwikihtml






def atpic_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    # http://docutils.sourceforge.net/docutils/nodes.py
    # http://docutils.sourceforge.net/docutils/parsers/rst/roles.py
    # http://docutils.sourceforge.net/docutils/parsers/rst/directives/images.py
    yy=atpic.log.setname(xx,'atpic_role')
    
    atpic.log.debug(yy,'input=',(name, rawtext, text, lineno, inliner,options,content))
    
    # inliner: http://doughellmann.com/2010/05/09/defining-custom-roles-in-sphinx.html
    atpic.log.debug(yy,'XXXXXinliner.document.settings.env',inliner.document.settings)
    firstpass=inliner.document.settings.atpic_firstpass # read-only
    atpic.log.debug(yy,'firstpass=',firstpass) # read-only
    atpic.log.debug(yy,'references=',inliner.document.settings.atpic_references) # read-write
    if firstpass: # just fill a dictionary
        atpic.log.debug(yy,'as we are in first pass, just set key',text)
        inliner.document.settings.atpic_references[text]=True
        return ([], [])
    else: # use the dictionary filled at first pass
        references=inliner.document.settings.atpic_references
        atpic.log.debug(yy,'references (read-only)=',references)
        try:
            (node_list,error_list)=references[text]
            if len(error_list)>0:
                msg = inliner.reporter.error(error_list[0], line=lineno)
                prb = inliner.problematic(rawtext, rawtext, msg)
                return ([prb], [msg])
            else:
                return references[text]
        except:
            atpic.log.error(yy,traceback.format_exc())
            return ([],[])



def convert(text,hxplo,pxplo,db,aid,uid,environ):
    yy=atpic.log.setname(xx,'convert')
    atpic.log.debug(yy,'input=',text,hxplo.list(),pxplo.list(),db,aid,uid,environ)

    wikipage=pxplo.getmatrix(0,1)
    wikipage=wikipage.decode('utf8')
    references={} # array to store the references
    firstpass=True

    docutils.parsers.rst.roles.register_canonical_role('atpic', atpic_role)
    docutils.parsers.rst.roles.DEFAULT_INTERPRETED_ROLE = 'atpic'
    


    # initialize mysettings:
    atpic.log.debug(yy,'INITIALIZE settings')
    mysettings={
            'stylesheet_path': None,
            'link-stylesheet': False,
            'embed_stylesheet': False,
            'file_insertion_enabled': False, # security!!!!!!!!
            'raw_enabled': False, # security!!!!!
            '_disable_config': True,
            'halt_level': 6,
            'atpic_editlinks':True,
            'atpic_wikipage':wikipage,
            'atpic_firstpass': True,
            'atpic_references': {},
        }
    atpic.log.debug(yy,'mysettings=',mysettings)


    # a dummy pass
    atpic.log.debug(yy,'FIRST PASS')
    (thehtml,mysettings)=doparse(text,mysettings)

    references=mysettings['atpic_references']
    atpic.log.debug(yy,'references=',references)



    atpic.log.debug(yy,'TRANSFORMING REFERENCES')
    references=transform_ref(references) # can be Unit tested
    atpic.log.debug(yy,'TRANSFORMING REFERENCES USING SQL')
    references=transform_refsql(db,references,hxplo,pxplo,aid,uid,environ) # has side effects, needs SQL
    atpic.log.debug(yy,'references=',references)
    atpic.log.debug(yy,'TRANSFORMING REFERENCES USING DOCUTILS NODES')
    references=transform_refnodes(references) # can be unit tested
    atpic.log.debug(yy,'references=',references)

    # a 2nd parsing, no sql needed
    atpic.log.debug(yy,'SECOND PASS')
    mysettings['atpic_firstpass']=False
    mysettings['atpic_references']=references
    atpic.log.debug(yy,'mysettings=',mysettings)
    (thehtml,mysettings)=doparse(text,mysettings)
    atpic.log.debug(yy,'output=',thehtml)
    return thehtml

def extract_wikitext(hxplo,pxplo):
    # easy to unit test
    yy=atpic.log.setname(xx,'extract_wikitext')


def postprocessing(db,hxplo,pxplo,actions,xmlo,aid,uid,environ):
    yy=atpic.log.setname(xx,'postprocessing')
    atpic.log.debug(yy,'input=',(hxplo.list(),pxplo.list(),actions,xmlo,aid,uid,environ))
    needwikihtml=get_needwikihtml(hxplo,pxplo)
    if needwikihtml:
        atpic.log.debug(yy,'this is a wiki main page')
        xml_string=b''.join(xmlo.data.content)
        atpic.log.debug(yy,'xml_string=',xml_string)
        xml_doc = etree.parse(io.BytesIO(xml_string))
        wtext=xml_doc.find('wikitext')
        atpic.log.debug(yy,'wtext=',wtext)
        if wtext is None:
            atpic.log.debug(yy,'empty wikitext')
        else:
            atpic.log.debug(yy,'we found some wtext')
            wikitext=wtext.text

            atpic.log.debug(yy,'wikitext=',wikitext)
            atpic.log.debug(yy,'hxplo.keys()=',hxplo.keys())
            if hxplo.keys()==[b'atpiccom',]:
                atpic.log.debug(yy,'setting uid to one')
                uid=b'1'
            if wikitext: 
                whtml=etree.Element("wikihtml")    
                wikihtml=convert(wikitext,hxplo,pxplo,db,aid,uid,environ) # actual conversion
            
                node=etree.XML(wikihtml) # create from string
                whtml.append(node)
                wtext.getparent().append(whtml)
                xml_string=etree.tostring(xml_doc)
                atpic.log.debug(yy,'xml_string=',xml_string)
                
                xmlo.data.content=[xml_string,]
                xmlo.data.stack=[]
    else:
        atpic.log.debug(yy,'no wiki needed')


    atpic.log.debug(yy,'output=',xmlo)

    return xmlo


if __name__ == "__main__":
    import atpic.libpqalex
    db=atpic.libpqalex.db_native()
    text=b"""
Title1
======
Subtitle
--------
some *bold* text.

1) one
2) two

paragraph
`hello`
see :RFC:`2822`.
some <b>html tags</b>
a < b
picture 1234 is coded as `p:1234`
some escaped \`role\`
picture 123 is coded as :atpic:`p:123`
now the first pic is `p:1`

subtitle2
---------
some text
`p:<script/>`
"""


    text=b'go to `test2` and `test3|a Test 3` now `p:1`'
    print('hi')
    hxplo=atpic.xplo.Xplo([])
    pxplo=atpic.xplo.Xplo([(b'wiki',b'some/wikipage'),])
    aid=b''
    uid=b'1'
    environ={}
    print(convert(text,hxplo,pxplo,db,aid,uid,environ))
    print(convert(text,hxplo,pxplo,db,aid,uid,environ))
    # print(convert_xml(text))
