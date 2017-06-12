#!/usr/bin/python3
# inspired by git
# content adressable:
# SHA1
# /a/b/cdefghijklm
# it contains a document compressed which SHA1 is the filename
# we log in a simple text file
# so that we can propagate changes to a remote server easily
# no management of conflicts, easy to inject into a db
# nosql
# grep the log file

# log file format:
# fname|date
# e.g:
# api|1221121221121|sha1|project
# keyword|timestamp|DELETE|project
# or
# timestamp|filename|sha1|project (optional)
# to do sort on timestamp

# how do we do branches? moves? redirect?
# put more than one project?
# 2 typical operations:
# all revs for one path
# last version of a path
# links pointing here

# can plug several storages
# on disk: easy
# in redis, memcached, sql, sqllite, elasticsearch, etc... for speed
 
# Problem of GIT: cannot have a large number (say 10k) files in one tree level
# wiki can 

# utilities:
# check (checks if that file is already in the SHA1 store
# checklast (checks if that file in already in sha1 and that the last version)

# journal allows to create fast indexes (elasticsearch)
# typical: on the web use elastic search; on the laptop: use log file + grep

# can use 'rsync' on the sha1 folder

# historical notes:
# store the FAQ and news in code, but each time we need to publish
# need to be able to publish only FAQ and news
# need to be able to stage

# need also to be able to change online

import sys
import os
import hashlib
import time
import datetime

def init(adir):
    # create a .gita folder
    print('creating .gita directory in',adir)
    os.mkdir(adir+"/.gita")

def parse_args():
    print('argv:',sys.argv)
    if sys.argv[1]=='init':
        adir=os.getcwd()
        init(adir)

def store_object(path,content):
    # get SHA1 of content and gzip it
    m = hashlib.sha1()
    m.update(content)
    # sha1=m.digest()
    sha1=m.hexdigest()
    print(sha1)
    # store it on disk
    # append action to journal

def perf():
    path=os.getcwd()+"/.gita"
    content="hello"
    for i in range(0,100):
        content=content+str(i)
        # print(content)
        store_object(path,content.encode('utf8'))

if __name__ == "__main__":
    print("Hi")

    print('argv:',sys.argv)
    print('pwd:',os.getcwd())
    # parse_args()
    perf()
    timenow=time.time()
    print('timenow',timenow)
    datetimefirst=datetime.datetime.fromtimestamp(timenow)
    print(datetimefirst)
