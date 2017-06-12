"""
read XMP xml files

"""
# see http://www.xml.com/lpt/a/1107
# see also raptor-utls
# rapper -o ntriples http://planetrdf.com/guide/rss.rdf
# rapper -o ntriples ../tests/fixture/xmp/sample_xmp.rdf
from rdflib.TripleStore import TripleStore
from rdflib.Namespace import Namespace

ns_dc=Namespace("http://purl.org/dc/elements/1.1/")
ns_pr=Namespace("http://prismstandard.org/1.0#")
store = TripleStore()
store.load("../tests/fixture/xmp/sample_xmp.rdf") 

# print dir(store)

quit()
# For all triples that have prism:publicationTime as their predicate,
for s,o in store.subject_objects(ns_pr["publicationTime"]):
    # if the triples' object is greater than the cutoff date,
    if o > cutOffDate:
        # print the date, author name, and title.
        print o,
        for object in store.objects(s, ns_dc["creator"]): 
            print object + ": ",
        for object in store.objects(s, ns_dc["title"]): 
            print object 

