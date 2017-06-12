"""
Maps (fuse) file system calls into tokyo table database queries

This will return XML strings.

The Fuse will use those XML
using a server

tokyo_server

"""

import tc 

def open():
    tdb=tc.TDB("/tokyo/tokyofs.tct", tc.TDBOWRITER | tc.TDBOCREAT)
    return tdb

def stat(dbh,uri):
    """
    stat for the uri
    Forges a XML packet withthe stat information
    """
    answer_list=[]
    answer_list.append("<sizeb>999999</sizeb>")
    answer_list.append("<pid>66666</pid>")
    return "".join(answer_list)

def pathget(dbh,path):
    """
    username based
    uid based
    Fuse needs to be mounted in /fusemnt
    
    """
    
