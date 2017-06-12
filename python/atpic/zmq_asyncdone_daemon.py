#!/usr/bin/python3

import atpic.daemonize
import atpic.zmq_asyncdone_server

atpic.daemonize.start(atpic.zmq_asyncdone_server.main_loop,'/var/run/zmq_asyncdone.pid')
