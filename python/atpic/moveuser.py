# syntax: moveuser.py -u UID -s STOREID

import sys, getopt

#for backtick operator equivalent
import commands

import re

optlist, list = getopt.getopt(sys.argv[1:], 'u:s:')
print "optlist =", optlist
print "list =", list
for option in optlist:
    print option
    if option[0] == '-u':
        user=option[1]
    if option[0] == '-s':
        store=option[1]


print "syncing user %s to store %s" % (user,store)

