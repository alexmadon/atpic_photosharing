"""
Xploded path and host
a list of pairs

[('objectname',id),]

"""
# import logging
import atpic.log

xx=atpic.log.setmod("INFO","xplo")



class Xplo():
    """
    Mainly unmutable class: optimized for read access
    """
    def __init__(self,alist):
        yy=atpic.log.setname(xx,'__init__')
        self.alist=alist
        atpic.log.debug(yy,self.alist)
        self.akeys=[]
        self.avalues=[]
        self.adic={}
        
        for (key,value) in alist:
            self.adic[key]=[]
            self.akeys.append(key)
            self.avalues.append(value)

        atpic.log.debug(yy,self.akeys)
        sig=[]
        for (key,value) in alist:
            self.adic[key].append(value)
            sig.append(key)
            if value:
                sig.append(b"_")
            else:
                if key==b'wiki': # wiki '' is allowed
                    sig.append(b"_")
                else:
                    sig.append(b"/")

        self.asignature=b"".join(sig)

    def keys(self):
       return self.akeys

    def list(self):
        return self.alist

    def items(self):
        return self.alist

    def signature(self):
        return self.asignature

    def toxml(self):
        xml=b''
        for (key,value) in self.alist:
            if value:
                value=value.replace(b'&',b'&amp;')
                xml=xml+b'<'+key+b'>'+value+b'</'+key+b'>'
            else:
                xml=xml+b'<'+key+b'/>'
        return xml

    def values(self):
        return self.avalues

    def getkey(self,key,pos=0):
        # there may be more than one object with that key e.g:
        # [('gallery',1),('gallery',2)]
        try:
            val=self.adic[key][pos]
        except:
            val=None
        return val

    def get(self,key,default=b''):
        # there may be more than one object with that key e.g:
        # [('gallery',1),('gallery',2)]
        # now takes the first one but control the default
        try:
            val=self.adic[key][0]
        except:
            val=default
        return val


    def __getitem__(self,key):
        return self.getkey(key)

    def __str__(self):
        return self.alist.__str__()

    def haskey(self,key):
        if key in self.akeys:
            return True
        else:
            return False

    def __len__(self):
        return len(self.alist)

    def getkeyall(self,key):
        """
        returns the lsit of all the values
        """
        if self.haskey(key):
            return self.adic[key]
        else:
            return []

    def getmatrix(self,i,j):
        try:
            val=self.alist[i][j]
        except:
            val=None
        return val
   

    def int(self):
        """
        converts to int the values
        creates a new object
        """
        nalist=[]
        for key,val in self.alist:
            try:
                nval=int(val)
                nalist.append((key,nval))
            except:
                nalist.append((key,val))

        return Xplo(nalist)
        
