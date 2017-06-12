#!/usr/bin/python3
import os
import sys
import getopt
import subprocess
import socket
"""

moves a (list of) artists to a server id
-l (list) coma separated of artist id
-t (to) id of the server (usually you are logged on this one)


"""

# os.system(cmd) better than result, varName=commands.getstatusoutput(acommand)
# import commands

def db():
    """
    Sets a db object that knows about the catgery of SQL requests 
    we use fo atpic
    """
    import os.path
    import postgresql.lib
    import postgresql.sys
    libdir=os.path.dirname(__file__)
    postgresql.sys.libpath.append(libdir+"/sql")
    lib=postgresql.lib.load("atpicdb")
    cat=postgresql.lib.Category(lib)
    # WARNING: true Database!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    # with ssh tunnel
    #  http://developer.postgresql.org/pgdocs/postgres/ssh-tunnels.html
    # ssh -L 63333:localhost:5432 www-data@user6.atpic.com
    db=postgresql.open("pq://dbuser:dbpasswd@localhost:63333/dbname",category=cat)

    return db

# http://python.projects.postgresql.org/

def get_id_from_artistid(db,artistid):
    query="select * from storing where id=(select storefrom from artist where id=$1)"
    print('#', query)
    statement=atpic.libpqalex.pq_prepare(db,'statement',query)
    with db.xact():
        row=statement(int(artistid))
        print('#',row)
        return row[0]

def get_storing_details_from_storingid(db,storingid):
    query="select * from storing where id=$1"
    print('#',query)
    statement=atpic.libpqalex.pq_prepare(db,'statement',query)
    with db.xact():
        row=statement(int(storingid))
        print('#',row)
        return row[0]

def get_artist_list_of_int(artist_list):
    """ 
    converts a coma separated string to a list of int
    """
    artist_list2=artist_list.split(',')
    print('#',artist_list2)
    # list comprehension:
    artist_list3=[int(elem) for elem in artist_list2]
    print('#',artist_list3)
    return artist_list3


if __name__ == "__main__":
    optlist, list = getopt.getopt(sys.argv[1:], 'l:t:f:')
    print ("optlist =", optlist)
    print ("list =", list)
    artist_list=""
    to_store=""
    from_store=""
    for option in optlist:
        print (option)
        if option[0] == '-l':
            artist_list=option[1]
        if option[0] == '-t':
            to_store=option[1]
        if option[0] == '-f': # overwrite the from
            from_store=option[1]

    if artist_list=="" or to_store=="":
        print("You need an artist list (-l) and a to (-t) destination id")
        quit()

    artist_list_of_int=get_artist_list_of_int(artist_list)

    storingid=int(to_store)
    for artistid in artist_list_of_int:
        print("=========================================================")
        print ("Doing artist",artistid)
        print("connecting to db....")
        mydb=db()

        if from_store!="":
            row_from=get_storing_details_from_storingid(mydb,from_store)
        else:
            row_from=get_id_from_artistid(mydb,artistid)

        servername_from=row_from["servername"]
        fastdir_atpic_from=row_from["fastdir_atpic"]

        row_to=get_storing_details_from_storingid(mydb,storingid)
        servername_to=row_to["servername"]
        fastdir_atpic_to=row_to["fastdir_atpic"]

        print("from",servername_from,fastdir_atpic_from)
        print("to",servername_to,fastdir_atpic_to)


        hostname=socket.gethostname()
        print("my host name is",hostname)
        # hostname="user1.atpic.com"
        if servername_to!=hostname:
            print("PLEASE LOG on",servername_to)
            quit()

    
        cmd="rsync -ave ssh --numeric-ids --group "+servername_from+":"+fastdir_atpic_from+"/"+"{0}".format(artistid)+" "+fastdir_atpic_to
        print(cmd)
        # os.system(cmd) # Alex

        mydb.close()

    quit()


    # get_id_from_artistid(db,1)
    
    # rsync -ave ssh --numeric-ids --group $rsyncfrom $rsyncto  0>&1 2>&1 >> /tmp/0synclog
    
