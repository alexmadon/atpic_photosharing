#!/usr/bin/python3
"""
Expands the wurfl XML with all devices properties listed

Logs to stderr
Sends to stdout a JSON file that can be POSTed to elasticsearch

"""
# import logging
import atpic.log
from xml.dom import minidom
from xml.etree.ElementTree import ElementTree
from lxml import etree # the fastest!!!!!!!!!!


xx=atpic.log.setmod("INFO","wurflex")



filename=b"/home/madon/public_html/perso/entreprise/sql_current/site/atpic/config/conf/wurfl/wurfl-2.2.xml"

"""
<group id="display">
      <capability name="physical_screen_height" value="27"/>
      <capability name="columns" value="11"/>
      <capability name="dual_orientation" value="false"/>
      <capability name="physical_screen_width" value="27"/>
      <capability name="rows" value="6"/>
      <capability name="max_image_width" value="90"/>
      <capability name="resolution_height" value="40"/>
      <capability name="resolution_width" value="90"/>
      <capability name="max_image_height" value="35"/>
</group>
"""

def capa2scan():
    return [
        (b'max_image_width',b'mw'),
        (b'max_image_height',b'mh'),
        (b'resolution_width',b'rw'),
        (b'resolution_height',b'rh'),
        (b'is_wireless_device',b'iw'),
        (b'xhtml_support_level',b'xs'),
        (b'preferred_markup',b'pm'),
        ]

def first_pass(filename):
    yy=atpic.log.setname(xx,'first_pass')
    dic={} # stores the device details
    listdev=[] # lists the device (ordered as in the XML file)
 

    # parse the xml file and store it in memory
    atpic.log.debug(yy,'parsing',filename)
    tree = etree.parse(filename)
    # print(dir(tree))
    listcapa=capa2scan()
    listcapa_first=[]
    for (a,b) in listcapa:
        listcapa_first.append(a)
    atpic.log.debug(yy,'listcapa',listcapa)
    for node in tree.iter(b'device'):
        # atpic.log.debug (node.tag, node.attrib)
        device = node.attrib.get(b'id').encode('utf8')
        fall_back = node.attrib.get(b'fall_back').encode('utf8')
        user_agent = node.attrib.get(b'user_agent').encode('utf8')
        # atpic.log.debug(yy,device,fall_back,user_agent)
        listdev.append(device)
        capa={}
        # for child in node.iter():
        #    atpic.log.debug(yy,'CHILD',child)
        for child in node.iter(b'capability'):
            # atpic.log.debug(yy,'CHILD',child)
            name = child.attrib.get(b'name').encode('utf8')
            if name in listcapa_first:
                value = child.attrib.get(b'value').encode('utf8')
                # atpic.log.debug(yy,name,value)
                capa[name]=value
        dic[device]={b'fall_back':fall_back,b'user_agent':user_agent,b'capa':capa}
    return (listdev,dic)


def set_capa(dic,device,capaname,capa):
    yy=atpic.log.setname(xx,'set_capa')
    if device==b'generic':
        return None
    atpic.log.debug(yy,'doing ',device,capaname)
    newcapa=dic[device][b'capa']
    if capaname in newcapa.keys():
        capavalue=newcapa[capaname]
        atpic.log.debug(yy,'stopping: device',device,'has',capaname,'=',capavalue)
    else:
        atpic.log.debug(yy,'recurse....')
        capavalue=set_capa(dic,dic[device][b'fall_back'],capaname,capa)
    return capavalue
                       
def second_pass(listdev,dic):
    yy=atpic.log.setname(xx,'second_pass')
    atpic.log.debug(yy,'doing 2nd')
    listcapa=capa2scan()
    for device in listdev: # device is a device id
        atpic.log.debug(yy,'')
        atpic.log.debug(yy,'==========================')
        atpic.log.debug(yy,'device %s ' % device)
        capa=dic[device][b'capa']
        atpic.log.debug(yy,'current capa dic %s' % capa)
        for (capaname,capashort) in listcapa:
            if capaname not in capa.keys():
                capavalue=set_capa(dic,device,capaname,capa)
                atpic.log.debug(yy,'Found setting %s=%s'%(capaname,capavalue))
                capa[capaname]=capavalue
                dic[device][b'capa']=capa
    return dic

def sxml(s):
    """
    TRansforms a string into valid XML
    """
    s=s.replace(b'&',b'&amp;')
    s=s.replace(b'"',b'&quot;')
    s=s.replace(b'<',b'&lt;')
    return s

def sxmlw(s):
    """
    To be used with Solr white space tokenizer
    """
    s=sxml(s)
    # s=s.replace('&',' ')
    # s=s.replace('"',' ')
    # s=s.replace('<',' ')
    # s=s.replace('-',' ')
    # s=s.replace('_',' ')
    # s=s.replace('/',' ')
    # s=s.replace('=',' ')
    # s=s.replace('?',' ')
    # s=s.replace('.',' ')
    # s=s.replace(';',' ')
    # s=s.replace(':',' ')
    # s=s.replace(b'(',b' ')
    # s=s.replace(b')',b' ')
    return s


def final_pass(listdev,dic):
    out=[]
    for device in listdev: # device is a device id
        # print('XXX %s' % dic[device])
        adev=dic[device]
        if adev[b'user_agent'].startswith(b'DO_NOT_MATCH'):
            # we ignore those negations
            pass
        else:
            acapa=adev[b'capa']
            outc=[]
            # outc.append(myout(b'id',sxml(device)))
            outc.append(myout(b'fb',sxml(adev[b'fall_back'])))
            outc.append(myout(b'ua',sxmlw(adev[b'user_agent'])))
            for (capaname,capashort) in capa2scan():
                outc.append(myout(capashort,sxml(acapa[capaname])))
                
            out.append(b'{ "index" : { "_index" : "wurfl", "_type" : "agent", "_id" : "'+sxml(device)+b'"}}')
            out.append(b'{ '+b', '.join(outc)+b' }')
    output=b'\n'.join(out)
    print(output.decode('utf8'))

def myout(fname,fnvalue,jsxm=b'json'):
    if jsxm==b'xml':         
        outs=b'<field name="'+fname+b'">'+fnvalue+b'</field>'
    else:
        outs=b'"'+fname+b'" : "'+fnvalue+b'"'
    return outs

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    (listdev,dic)=first_pass(filename)
    dic=second_pass(listdev,dic)
    # final print
    final_pass(listdev,dic)
