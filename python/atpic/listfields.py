#!/usr/bin/python3
"""
This module is complementary of the model:
it list fields to be displayed in forms.
It could be merged with the model.

you could use the COMMENT command on sql objects to store this info


user:
-----
password should not be displayed publicly
email either
uname either


gallery:
-------
secret either


"""

from lxml import etree
from io import StringIO

import atpic.model_pystring

def get_xml_model():
    # xml_doc = etree.parse("tt.xml")
    xml_doc=etree.parse(StringIO(atpic.model_pystring.getmodel()))
    return xml_doc

def get_fields(table,fieldval):
    thelist=list()
    xml_doc = get_xml_model()
    print(dir(xml_doc))
    atable = xml_doc.find("/table[@name='%s']" % table)  
    if atable==None:
        raise Exception("Table not found",table)
    # print(p)
    # print(dir(p))
    # read = p.attrib.get('read')
    # print(read)
    # for name, value in sorted(atable.attrib.items()):
    #    print ('  %-4s = "%s"' % (name, value))

    for node in atable.findall("attribute[@%s]" % fieldval): 
        # e.g.: "attribute[@name='id']"
        # print(dir(node))
        # print('TAG %s' % node.tag)
        # for name, value in sorted(node.attrib.items()):
        #    print ('  %-4s = "%s"' % (name, value))
        fname=node.attrib['name']
        if fname[0]=='_':
            fname=fname[1:]
        thelist.append(fname)
    return thelist


def get_fields_read(table):
    return get_fields(table,"read='True'")

def get_fields_write(table):
    return get_fields(table,"write='True'")

if __name__ == "__main__":
    print(get_fields('_user_gallery',"read='True'"))
    print(get_fields_read('_user'))
    print(get_fields_write('_user_gallery_pic'))


