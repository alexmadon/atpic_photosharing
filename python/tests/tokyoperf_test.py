# -*- coding: utf-8 -*-
"""
Unit tests for Tokyo Cabinet

Compare the speed of the different drivers

Conclusion:
google tc is 5X faster than atpic ctypes implementation
"""
import unittest
import os
import time
import atpic.tokyoctypes as tc
import tc as tc2
import tokyo.cabinet as tc3
from pyrant import Tyrant, Q


"""
Compares speed of atpic.tokyo and tc

"""

import psyco # package python-psyco 
psyco.full()



class testTdbOpen(unittest.TestCase):
    
    def setUp(self):
        print "setUp"
        self.dbfile="casketperf.tct"
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)
            
    def tearDown(self):
        print "tearDown"
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)
            
    def testall(self):
        print "Hiiiii"
        # tdb=tc.Tdb()
        tdb=tc.TDB(self.dbfile, tc.TDBOWRITER | tc.TDBOCREAT)
        print tdb
        print tdb.tdb
        print "number of records in db: %s" % tdb.rnum()
        time1=time.time()
        # tdb.tranbegin()
        for i in range(1,1000000):
            tdb.put("key%s" %i ,{"firstname":"Alex","lastname":"Madon","age":34})
        # tdb.trancommit()


        time2=time.time()
        dt=time2-time1
        print "Atpic tc: %s" % dt

class testTdbOpen2(unittest.TestCase):
    
    def setUp(self):
        print "setUp"
        self.dbfile="casketperf.tct"
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)
            
    def tearDown(self):
        print "tearDown"
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)
            
    def testall(self):
        print "Hiiiii"
        # tdb=tc.Tdb()
        tdb=tc2.TDB(self.dbfile, tc.TDBOWRITER | tc.TDBOCREAT)
        
        # print "number of records in db: %s" % tdb.rnum()
        time1=time.time()
        for i in range(1,1000000):
            tdb.put("key%s" %i ,{"firstname":"Alex","lastname":"Madon","age":"34"})

        time2=time.time()
        dt=time2-time1
        print "Google tc: %s" % dt

class testTdbOpen3(unittest.TestCase):
    """Uses http://bitbucket.org/lasizoillo/tokyocabinet/"""
    def setUp(self):
        print "setUp"
        self.dbfile="casketperf3.tct"
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)
            
    def tearDown(self):
        print "tearDown"
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)
            
    def testall(self):
        print "Hiiiii3"
        # tdb=tc.Tdb()
        tdb = tc3.TableDB()
        tdb.open(self.dbfile, tc.TDBOWRITER | tc.TDBOCREAT)
        
        # print "number of records in db: %s" % tdb.rnum()
        time1=time.time()
        for i in range(1,1000000):
            tdb.put("key%s" %i ,{"firstname":"Alex","lastname":"Madon","age":"34"})

        time2=time.time()
        dt=time2-time1
        print "bitbucket tc: %s" % dt


class testTdbTyrant(unittest.TestCase):
    """ You need to start tyrant:
    
    ttserver test.tct
    """
    def NOtestall(self):
        t = Tyrant(host='127.0.0.1', port=1978)
        time1=time.time()
        for i in range(1,10000):
            key="key%s" %i
            t[key]={"firstname":"Alex","lastname":"Madon","age":"34"}
        time2=time.time()
        dt=time2-time1
        print "Tyran tc: %s" % dt


if __name__=="__main__":
    unittest.main()
