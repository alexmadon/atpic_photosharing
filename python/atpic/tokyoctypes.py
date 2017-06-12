# -*- coding: utf-8 -*-
import ctypes
# libtokyocabinet.so
ctypes.cdll.LoadLibrary("/usr/local/lib/libtokyocabinet.so")
libtokyocabinet = ctypes.CDLL("/usr/local/lib/libtokyocabinet.so")


# http://tokyocabinet.sourceforge.net/spex-en.html
# The Table Database API
# tctdb.h


# constants from tctdb.h
TDBOREADER = 1 << 0 # open as a reader 
TDBOWRITER = 1 << 1 # open as a writer 
TDBOCREAT = 1 << 2 # writer creating 
TDBOTRUNC = 1 << 3 # writer truncating 
TDBONOLCK = 1 << 4 # open without locking 
TDBOLCKNB = 1 << 5 # lock without blocking 
TDBOTSYNC = 1 << 6 # synchronize every transaction 



# enumeration for query conditions
TDBQCSTREQ=0  #  string is equal to
TDBQCSTRINC=1  #  string is included in
TDBQCSTRBW=2  #  string begins with
TDBQCSTREW=3  #  string ends with
TDBQCSTRAND=4  #  string includes all tokens in
TDBQCSTROR=5  #  string includes at least one token in
TDBQCSTROREQ=6  #  string is equal to at least one token in
TDBQCSTRRX=7  #  string matches regular expressions of
TDBQCNUMEQ=8  #  number is equal to
TDBQCNUMGT=9  #  number is greater than
TDBQCNUMGE=10  #  number is greater than or equal to
TDBQCNUMLT=11  #  number is less than
TDBQCNUMLE=12  #  number is less than or equal to
TDBQCNUMBT=13  #  number is between two tokens of
TDBQCNUMOREQ=14  #  number is equal to at least one token in
TDBQCNEGATE = 1 << 24  # negation flag
TDBQCNOIDX = 1 << 25 # no index flag


# enumeration for order types 
TDBQOSTRASC=0   #  string ascending 
TDBQOSTRDESC=1   #  string descending 
TDBQONUMASC=2   #  number ascending 
TDBQONUMDESC=3   #  number descending 




class TDB:
    """
    Tdb has some similarties with the dict python type
    Some we implement some of the dict methods
    """
    def __init__(self,filename,flags):
        self.tdb = libtokyocabinet.tctdbnew()
        # libtokyocabinet.tctdbopen(tdb, "casket.tct", TDBOWRITER | TDBOCREAT)
        ret=libtokyocabinet.tctdbopen(self.tdb, filename, flags)
        # print "retdb=%s" % ret

    def put(self,pkey,cols):
        """pkey is the primary key, cols is the map"""
        pksiz = len(pkey)
        if isinstance(cols,dict):
            # print "This is a dict"
            cols=Map(cols)
        elif not isinstance(cols,Map):
            raise "Expects a Map or a dict"
        # print "type of cols is %s" % type(cols)
        libtokyocabinet.tctdbput(self.tdb, pkey, pksiz, cols.cols)


    def get(self,pkey):
        rbuf=pkey
        rsiz=len(pkey)
        cols = libtokyocabinet.tctdbget(self.tdb, rbuf, rsiz);
        print "cols is %s" %cols
        if cols == 0:
            return {}
        else:
            res=Map()
            res.cols=cols
            return res

    def __getitem__(self,pkey):
        return self.get(pkey)

    def close(self):
        # close the database
        libtokyocabinet.tctdbclose(self.tdb) # returns bool

    def __del__(self):
        # print "Tdb.__del__"
        # delete the object
        libtokyocabinet.tctdbdel(self.tdb)


    def tranbegin(self):
        return libtokyocabinet.tctdbtranbegin(self.tdb)
    def trancommit(self):
        return libtokyocabinet.tctdbtrancommit(self.tdb)
    def tranabort(self):
        return libtokyocabinet.tctdbtranabort(self.tdb)


    def path(self):
        return libtokyocabinet.tctdbpath(self.tdb)
    def rnum(self):
        return libtokyocabinet.tctdbrnum(self.tdb)

    def fsiz(self):
        return libtokyocabinet.tctdbfsiz(self.tdb)

    def setindex(self,name,itype):
        return libtokyocabinet.ctdbsetindex(self.tdb, name, itype);

class TdbQuery:
    def __init__(self,tdb):
        """Expects an instance of the Tdb class"""
        self.qry=libtokyocabinet.tctdbqrynew(tdb.tdb)
    def search(self):
        res = libtokyocabinet.tctdbqrysearch(self.qry)
        return List(res)

    def addcond(self,field,operator,expression):
        libtokyocabinet.tctdbqryaddcond(self.qry,field,operator,expression)

    def setlimit(self,max,skip):
        libtokyocabinet.tctdbqrysetlimit(self.qry,max,skip)

    def setindex(self,name,itype):
        libtokyocabinet.tctdbsetindex(self.qry,name,itype);

    def setorder(self,field,sorttype):
        libtokyocabinet.tctdbqrysetorder(self.qry,field,sorttype)

    def __del__(self):
        # print "Qry.__del__"
        libtokyocabinet.tctdbqrydel(self.qry)

    def searchout(self):
        """The function `searchout' is used in order to remove each record corresponding to a query object."""
        libtokyocabinet.tctdbqrysearchout(self.qry)


class List:
    """
    This is list, so we implement of of the list methods:
    http://www.python.org/doc/2.5.2/ref/sequence-types.html
    http://www.python.org/doc/2.5.2/lib/typesseq.html
    """
    def __init__(self,thelist):
        self.tclist=thelist
        
    def __len__(self):
        return libtokyocabinet.tclistnum(self.tclist)

    def __getitem__(self,i):
        """i is an integer giving the psotion of the (pkey,map) in the list"""
        rsiz = ctypes.c_int()
        rbuf = libtokyocabinet.tclistval(self.tclist, i, ctypes.byref(rsiz));
        print "rbuf is %s" %rbuf
        mvalue=ctypes.c_char_p(rbuf)

        return mvalue.value
    def __del__(self):
        # print "List.__del__"
        libtokyocabinet.tclistdel(self.tclist)


class Map:
    """
    We implement the methods for a python mapping (dict)
    http://www.python.org/doc/2.5.2/ref/sequence-types.html 
    http://www.python.org/doc/2.5.2/lib/typesmapping.html
    """
    def __init__(self,adict=None):

        if adict is None:
            self.cols=libtokyocabinet.tcmapnew()
        else:
            if isinstance(adict,dict):
                self.cols=libtokyocabinet.tcmapnew()
                for key in adict:
                    self.put(key,adict[key])
            else:
                raise "Map() or Map(dict) only"
        
    def put(self,name,value):
        name=str(name)
        value=str(value)
        libtokyocabinet.tcmapput2(self.cols,name,value);

    def get(self,name):
        name=str(name)
        value=libtokyocabinet.tcmapget2(self.cols, name)
        mvalue=ctypes.c_char_p(value)
        return mvalue.value
    
    
    # see special functions p 392 of python scripting
    
    # see "Emulating container types"
    # http://www.python.org/doc/2.5.2/ref/sequence-types.html
    # Containers usually are sequences (such as lists or tuples) 
    # or mappings (like dictionaries)
    def __getitem__(self,name):
        name=str(name)
        value=libtokyocabinet.tcmapget2(self.cols, name)
        mvalue=ctypes.c_char_p(value)
        return mvalue.value
    
    def __setitem__(self,name,value):
        name=str(name)
        value=str(value)
        libtokyocabinet.tcmapput2(self.cols,name,value);
        
    def __len__(self):
        return libtokyocabinet.tcmaprnum(self.cols)
    
    
    def __iter__(self):
        
        # print "calling __iter__"
        self.index=0
        self.len=libtokyocabinet.tcmaprnum(self.cols)
        libtokyocabinet.tcmapiterinit(self.cols)
        return self
    
    def next(self):
        # print "self.cols1 %s" % self.cols
        if self.index< self.len:
            # print "++++++++++ iteration %s/%s +++++++++++++++++" % (self.index,self.len)
            self.index += 1
            name=libtokyocabinet.tcmapiternext2(self.cols)
            mname=ctypes.c_char_p(name)
            # print "mname===%s" % mname.value
            # print self.get(mname.value)
            # value=libtokyocabinet.tcmapget2(self.cols, mname.value)
            # print value
            # mvalue=ctypes.c_char_p(value)
            # print "mvalue=" % mvalue
            # return self.get(mname.value)
            return mname.value
        else:
            raise StopIteration
        
        
    def keys(self):
        """a.keys(): a copy of a's list of keys"""
        list=[]
        for key in self:
            list.append(key)
        return list
    
    def values(self):
        """a.values(): a copy of a's list of values"""
        list=[]
        for key in self:
            list.append(self[key])
        return list

    def items(self):
        """a.items(): a copy of a's list of (key, value) pairs"""
        list=[]
        for key in self:
            list.append((key,self[key]))
        return list

    def __del__(self):
        # print "Map.__del__"
        libtokyocabinet.tcmapdel(self.cols)
