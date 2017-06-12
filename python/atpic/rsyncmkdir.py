#!/usr/bin/python3
import os
import sys
import getopt
import subprocess
import socket

import rsyncpy

"""

moves a (list of) artists to a server id
-l (list) coma separated of artist id
-t (to) id of the server (usually you are logged on this one)


see www/_move_ln.php

"""


def get_galleries(db,artistid):
    query="select * from artist_gallery where refartist=$1 order by id"
    print('#',query)
    statement=atpic.libpqalex.pq_prepare(db,'statement',query)
    with db.xact():
        rows=statement(int(artistid))
        return rows

# os.system(cmd) better than result, varName=commands.getstatusoutput(acommand)
# import commands

if __name__ == "__main__":
    optlist, list = getopt.getopt(sys.argv[1:], 'l:t:f:')
    print ("# optlist =", optlist)
    print ("# list =", list)
    artist_list=""
    to_store=""
    from_store=""
    for option in optlist:
        print ('#',option)
        if option[0] == '-l':
            artist_list=option[1]
        if option[0] == '-t':
            to_store=option[1]
        if option[0] == '-f': # overwrite the from
            from_store=option[1]


    if artist_list=="" or to_store=="":
        print("You need an artist list (-l) and a to (-t) destination id")
        quit()

    artist_list_of_int=rsyncpy.get_artist_list_of_int(artist_list)

    storingid=int(to_store)
    actions=[]
    for artistid in artist_list_of_int:
        print("# =========================================================")
        print ("# Doing artist",artistid)
        print("# connecting to db....")
        mydb=rsyncpy.db()

        if from_store!="":
            row_from=rsyncpy.get_storing_details_from_storingid(mydb,from_store)
        else:
            row_from=rsyncpy.get_id_from_artistid(mydb,artistid)


        row_to=rsyncpy.get_storing_details_from_storingid(mydb,storingid)

        servername_to=row_to["servername"]
        fastdir_atpic=row_to["fastdir_atpic"]
        fastdir_atpic_ln=row_to["fastdir_atpic_ln"]

        print("# from",row_from)
        print("# to",row_to)

        hostname=socket.gethostname()
        print("# my host name is",hostname)

        # comment this out for real sync
        # hostname="user4.atpic.com"


        if servername_to!=hostname:
            print("# PLEASE LOG on",servername_to)
            # quit() # Alex



        # masterln
        actions.append("rm /atpicup/masterln/{artistid}".format(artistid=artistid))
        # clean the links
        actions.append("ln -s {fastdir_atpic_ln}/{artistid} /atpicup/masterln/{artistid}".format(fastdir_atpic_ln=fastdir_atpic_ln,artistid=artistid));
        
        rows=get_galleries(mydb,artistid)


        # print(rows)
        for row in rows:
            gid=row["id"]
            secret=row["secret"]
            if not secret:
                secret="0"
            print("# gallery",gid,"secret",secret)


            # the true dir with the pic should exist
            existing_dir="{fastdir_atpic}/{artistid}/{galleryid}/0".format(
                fastdir_atpic=fastdir_atpic,
                artistid=artistid,
                galleryid=gid)
            

            # the new (ln) dir
            newdir="{fastdir_atpic_ln}/{artistid}/{galleryid}".format(
                fastdir_atpic_ln=fastdir_atpic_ln,
                artistid=artistid,
                galleryid=gid)
            
        
            newlink="{fastdir_atpic_ln}/{artistid}/{galleryid}/{secret}".format(
                fastdir_atpic_ln=fastdir_atpic_ln,
                artistid=artistid,
                galleryid=gid,
                secret=secret)


            # gallery links
            
            actions.append("rm {newdir}/*".format(newdir=newdir)); # make sure there is no previous symlinks under that dir
            actions.append("mkdir -p {newdir}".format(newdir=newdir));
            actions.append("ln -s {existing_dir} {newlink}".format(existing_dir=existing_dir,newlink=newlink));

        # cmd="rsync -ave ssh --numeric-ids --group "+servername_from+":"+fastdir_atpic_from+"/"+"{0}".format(artistid)+" "+fastdir_atpic_to
        # print(cmd)
        # os.system(cmd)

        mydb.close()

    print("# =========== ACTIONS ===============")
    for action in actions:
        print(action)
        # os.system(action) # Alex



    print("# ======== next, you should ======")
    # print("FROM",row_from)

    # print("TO",row_to)

    print("# update artist set storefrom={to_store} where id={artistid};".format(
            to_store=to_store,
            artistid=artistid,
            ))
    print("# ssh {servername}".format(
            servername=row_from["servername"]
            ))
    print("# rm -rf {fastdir_atpic}/{artistid}".format(
            fastdir_atpic=row_from["fastdir_atpic"],
            artistid=artistid
            ))
    print("# rm -rf {fastdir_atpic_ln}/{artistid}".format(
            fastdir_atpic_ln=row_from["fastdir_atpic_ln"],
            artistid=artistid
            ))
    quit()


    # get_id_from_artistid(db,1)
    
    # rsync -ave ssh --numeric-ids --group $rsyncfrom $rsyncto  0>&1 2>&1 >> /tmp/0synclog
    
