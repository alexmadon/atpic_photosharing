# -*- coding: utf-8 -*-
"""Unit tests for Tokyo Cabinet"""
import unittest
import os
import atpic.tokyoctypes as tc



class testTdbOpen(unittest.TestCase):
    
    def setUp(self):
        print "setUp"
        self.dbfile="casket.tct"
        # if os.path.exists(self.dbfile):
        #     os.remove(self.dbfile)
            
    def tearDown(self):
        print "tearDown"
        # if os.path.exists(self.dbfile):
        #     os.remove(self.dbfile)
            
    def testall(self):
        print "Hiiiii"
        # tdb=tc.Tdb()
        tdb=tc.TDB(self.dbfile, tc.TDBOWRITER | tc.TDBOCREAT)
        print tdb
        print tdb.tdb
        print "number of records in db: %s" % tdb.rnum()

        # self.assertEqual(dispatcher[key],record[1][key])
    
        tdb.put("key12345",{"firstname":"Alex","lastname":"Madon","age":34})
        tdb.put("key12345b",{"firstname":"Alex","lastname":"Doe","age":44})

        cols=tc.Map()
        cols.put("firstname","John")
        cols.put("lastname","Doe")
        cols.put("age",72)
        tdb.put("key12346",cols)


        colget=tdb.get("key12346")
        print colget.items()

        colget=tdb.get("key12346a") # non existing key
        print colget.items()


        qry=tc.TdbQuery(tdb) # attach a new query to the database
        result_list=qry.search()

        print "length of res: %s" % len(result_list)


        for i in range(0,len(result_list)):
            pkey=result_list[i]
            print "record %s = %s" % (i,pkey)
            print tdb[pkey].items()

        # more query testing
        print "More query testing"
        qry=tc.TdbQuery(tdb) # attach a new query to the database
        qry.addcond("firstname",tc.TDBQCSTREQ,"Alex")
        qry.setorder("lastname",tc.TDBQOSTRASC)
        result_list=qry.search()

        print "length of res: %s" % len(result_list)


        for i in range(0,len(result_list)):
            pkey=result_list[i]
            print "record %s = %s" % (i,pkey)
            print tdb[pkey].items()

        print "number of records in db: %s" % tdb.rnum()


class testMap(unittest.TestCase):
    def NOtestall(self):
        cols=tc.Map()
        cols.put("name","Madon")
        value=cols.get("name")
        print value
        
        # call the __setitem__
        cols["age"]="34";
        # call the __getitem__
        print cols["age"]
        cols["weight"]=72 # call with an int, should be converted to ctypes.c_char_p
        print "hi"
        print cols["weight"]
        
        
        cols["accent"]="Clara cet été là"
        print cols["accent"]
        
        # test the iterator
        for key in cols:
            print "%s, %s" % (key,cols[key])
            
        print cols.keys()
        print cols.values()
        print cols.items()
        for (k,v) in cols.items():
            print k,v
            print "key=%s, value=%s" % (k,v)

        cols2=tc.Map({"firstname":"alex","lastname":"Madon"})
        print cols2.items()

if __name__=="__main__":
    unittest.main()
