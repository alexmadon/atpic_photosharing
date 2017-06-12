"""XML functions"""


from xml.dom import minidom
import cgi
import html
import atpic.log
import traceback
from atpic.mybytes import *
# import atpic.uni
xx=atpic.log.setmod("INFO","xmlat")

def extract_text_recurse(xmldoc,rc):
    """Function that recurses the nodes to get the text"""
    for node in xmldoc.childNodes:
        # print node
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
        rc = extract_text_recurse(node,rc)
    return rc


def extract_text(soup):
    """soup is any string
    see def getText(nodelist):
    http://docs.python.org/lib/dom-example.html
    """
    xmldoc = minidom.parseString(b"<soup>"+soup+b"</soup>")
    rc = extract_text_recurse(xmldoc,"")
    return rc.encode('utf8')


#
#
#

def extract_id(xml):
    """This returns a dictionnary of Phrase ID and Phrase in English
    Input is a XML string with some <t id="">bbbbb</t>"""
    yy=atpic.log.setname(xx,'extract_id')
    xmldoc = minidom.parseString(xml)
    wikis = xmldoc.getElementsByTagName("t")
    dict={}
    for wiki in wikis:
        atpic.log.debug(yy,'wiki',wiki.toxml())
        theid=wiki.attributes["id"].value
        theidb=theid.encode('utf8')
        childNodes=wiki.childNodes
        out=[] # we will store in a list (more efficient that a string)
        for child in childNodes:
            out.append(child.toxml())
        thevalue=''.join(out)
        thevalueb=thevalue.encode('utf8')
        dict[theidb]=thevalueb
        # print dict[theid]
    return dict




# based on cull_children
def replace_id_children(nodelist,inset,parent,dictids,wiki):
    yy=atpic.log.setname(xx,'replace_id_children')
    atpic.log.debug(yy,nodelist,inset,parent,dictids,wiki)

    try:
        # set the wiki attribute string
        if wiki==b"on":
            atpic.log.debug(yy,'wiki is on')
            wikistring=' wiki="on"'
        else:
            wikistring=''
        # process the nodes
        for subnode in nodelist:
            if (subnode.nodeType == subnode.ELEMENT_NODE):
                thetag = subnode.tagName
                # called = "" # in case it's not an img or title
                if (thetag == "t"):
                    theid=subnode.getAttribute("id")
                    atpic.log.debug(yy,'theid',theid)
                    theidb=theid.encode('utf8')
                    if theidb in dictids:
                        atpic.log.debug(yy,'theid is in dic')
                        repl='<t id="%s"%s>%s</t>' % (theid,wikistring,dictids[theidb].decode('utf8'))
                        atpic.log.debug(yy,'repl',repl)
                    else:
                        out=[]
                        atpic.log.debug(yy,'theid is NOT in dic')
                        for child in subnode.childNodes:
                            out.append(child.toxml())
                        repl='<t id="%s"%s missing="1">%s</t>' % (theid,wikistring,"".join(out))
                    repldoc=minidom.parseString(repl.encode("utf-8"))
                    subnode.parentNode.replaceChild(repldoc.firstChild,subnode)
                replace_id_children(subnode.childNodes," "+inset,subnode,dictids,wiki)
    except KeyError:
        # we leave the original text if no dictionnary
        atpic.log.error(yy,traceback.format_exc())
        pass
    




def replace_id(xml,dictids,wiki=b"off"):
    """Translates a XML string based on a translation dictionnary
xml input should contains <t id="ID">...</t> strings
dictids should be dictids[ID]="the translation"


ouput is xmstring with the content of the <t/> tags (elements) translate and optionally a wiki attribute added
"""
    # xml=atpic.uni.string(xml)
    xmldoc = minidom.parseString(xml)
    replace_id_children(xmldoc.childNodes,"",xmldoc,dictids,wiki)
    return xmldoc.toxml().encode('utf8')


# ==================================================================
# ESCAPE Functions
# Some format like RSS requires HTML to be escaped to be a valid RSS file
# ==================================================================


def escape_children(nodelist,parent,taglist):
    for subnode in nodelist:
        if (subnode.nodeType == subnode.ELEMENT_NODE):
            thetag = subnode.tagName
            # print "thetag is %s" %thetag
            # check if the tag is in the list of tags to escape
            if thetag in taglist:
                out=[]
                # get the xml within that tag
                for child in subnode.childNodes:
                    out.append(child.toxml())
                string2escape="".join(out)
                # and escape it
                # escaped_string=cgi.escape(string2escape)
                escaped_string=html.escape(string2escape)
                # print escaped_string
                # build a new node with the escaped content and the node name and attributes
                repl=[]
                repl.append("<%s" % thetag)
                for key in list(subnode.attributes.keys()):
                    repl.append(' %s="%s"' % (key,subnode.attributes[key].value))
                repl.append(">")
                repl.append(escaped_string)
                repl.append("</%s>" % thetag)
                repls="".join(repl)
                # print repls
                # then replace in the original tree the node by the escaped node
                repldoc=minidom.parseString(repls.encode("utf-8")) #XXXXXX
                subnode.parentNode.replaceChild(repldoc.firstChild,subnode)
            else:
                escape_children(subnode.childNodes,parent,taglist)

def escape_xml(xml,taglist):
    """
    xml is a string
    taglist is a list of tags: any xml subtree within that tage will be escaped.
    the rest of the xml tree is preserved
    """
    
    # xml=atpic.uni.string(xml)
    # print type(xml)
    xmldoc = minidom.parseString(xml)
    taglist=list2string(taglist)
    escape_children(xmldoc.childNodes,xmldoc,taglist)
    # dir(xmldoc.toxml)
    return xmldoc.toxml().encode('utf8')
