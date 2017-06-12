# apt-get install postgresql-plpython-8.1 

"""
postgres python functions



"""

importfct="""

CREATE OR REPLACE FUNCTION pyclean_load() returns text
    AS
'try:
 import xml
except Exception, ex:
 plpy.notice("import atpic.plpython -- %s" % str(ex))
 return "failed as expected"
return "succeeded, that wasn''t supposed to happen"'
LANGUAGE plpythonu;



select pyclean_load();

CREATE OR REPLACE FUNCTION pyunicode() returns text
AS
'

string="""Clara cet été là"""

return string
'
LANGUAGE plpythonu;


--cf http://www.pgcluster.org/svn/pgcluster-1.9/src/pl/plpython/sql/plpython_function.sql
CREATE OR REPLACE FUNCTION pyclean(text) returns text
    AS
$$from xml.dom import minidom

def extract_text_recurse(xmldoc,rc):
    for node in xmldoc.childNodes:
        # print node
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.toxml()
            # if you use .data instead of .toxml() you will escape entities
            pass
        rc = extract_text_recurse(node,rc)
    return rc


def extract_text(soup):
    if not soup:
        soup='' # avoid to see None
    soup_mod="<soup>%s</soup>" % soup
    xmldoc = minidom.parseString(soup_mod)
    rc=''
    rc = rc+extract_text_recurse(xmldoc,u"")
    # return xmldoc.toxml().encode( "utf-8" )
    return rc.encode("utf-8")

return extract_text(args[0])

$$
LANGUAGE plpythonu;


SELECT pyclean('alex is the <b>best</b>');
SELECT pyclean('Clara cet <i>été</i><!-- comment --> là');
SELECT pyclean(NULL);
SELECT pyclean('Alex &amp; Dama');
select aid,gid,pid,solr from select_flat_a(2);



"""

print importfct

