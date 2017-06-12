"""
read XMP xml files

"""


file_xml_hand=open("../tests/fixture/xmp/sample_xmp.rdf","r")
xml=file_xml_hand.read()
file_xml_hand.close()
print xml



from xml.dom import minidom

xmldoc = minidom.parseString(xml)
print xmldoc
print dir(xmldoc)
desc=xmldoc.getElementsByTagName("rdf:Description")
print desc
firstdesc=desc[0]
print firstdesc.attributes.keys()
print firstdesc.attributes.values()

# first do the simple properties
for key in firstdesc.attributes.keys():
    attr=firstdesc.attributes[key]
    print "key=%s" % key
    print "value=%s" % attr.value
    print "name=%s" % attr.name
    print "localName=%s" % attr.localName
    print "nodeName=%s" % attr.nodeName
    print "prefix=%s" % attr.prefix
    print "namespaceURI=%s" % attr.namespaceURI
    print dir(attr)


# quit()
# now the complex ones
for e in firstdesc.childNodes:
    
    if e.nodeType == e.ELEMENT_NODE:
        print e
        print dir(e)
        print "nodeName = %s" % e.nodeName
        print "namespaceURI = %s"% e.namespaceURI
        if e.hasAttributes:
            for key in e.attributes.keys():
                attr=e.attributes[key]
                print "++++++++++"
                print "key=%s" % key
                print "value=%s" % attr.value
                print "name=%s" % attr.name
                print "localName=%s" % attr.localName
                print "nodeName=%s" % attr.nodeName
                print "prefix=%s" % attr.prefix
                print "namespaceURI=%s" % attr.namespaceURI
        if e.hasChildNodes:
            print "Has child nodes"
