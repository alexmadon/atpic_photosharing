#!/usr/bin/python3

import atpic.daemonize
import atpic.zmq_elastic_server

atpic.daemonize.start(atpic.zmq_elastic_server.main_loop,'/var/run/zmq_elastic.pid')
