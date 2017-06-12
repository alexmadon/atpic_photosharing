import sys
import pycurl # debian package python-pycurl
from cStringIO import StringIO
import tidy

import atpic.solr
import atpic.uni

"""
Solr curl
"""

from xml.dom.ext import PrettyPrint
from StringIO import StringIO

def mytidynew(node, encoding='utf-8'):
    tmpStream = StringIO()
    PrettyPrint(node, stream=tmpStream, encoding=encoding)
    print tmpStream.getvalue()

def mytidy(xml):
    from xml.dom import minidom
    import sys
    xmldoc = minidom.parseString(xml.encode("utf-8")) # utf8 see http://evanjones.ca/python-utf8.html
    xmldoc.writexml(sys.stdout,addindent="  ", newl="\n") # may use toprettyxml

def mytidyold(xml_post):
    options = dict(output_xhtml=0, 
                   add_xml_decl=0, 
                   indent=1, 
                   tidy_mark=0)
    print tidy.parseString(xml_post, **options)

def solr_update(thetype,id):
    """ errors will appear in the script logs as:
    <title>Error 400 </title>
    """

    print "============================================"
    print "DOINGGGGGGGGG: thetype %s, id=%s" % (thetype,id)
    print "============================================"
    url="http://localhost:8983/solr/update";
    
    
    header = [ "Content-type:text/xml; charset=utf-8"];
    body = StringIO()
    c=pycurl.Curl()
    # $ch = cuRlq_init();
    xml_post=atpic.solr.solr_generate(thetype,id)

    # print xml_post.replace(">",">\n")
    print type(xml_post)
    c.setopt(c.URL, url);
    c.setopt(c.HTTPHEADER, header);
    # c.setopt(c.RETURNTRANSFER, 1);
    c.setopt(c.POST, 1);
    # print type(xml_post)

    c.setopt(c.POSTFIELDS, atpic.uni.string(xml_post)); # setopt expects a string
    c.setopt(c.VERBOSE, 1)
    c.setopt(c.WRITEFUNCTION, body.write)
    # c.setopt(c.HTTP_VERSION, CURL_HTTP_VERSION_1_1);
    # c.setopt(c.HEADER_OUT, 1);
    data=c.perform()
    c.close()
    contents = body.getvalue()
    print "********************************************"
    print contents

if __name__ == "__main__":
    for aid in range(1,1000):
        solr_update('a',aid)
    print "Committing..."
    print atpic.solr.solr_commit()
