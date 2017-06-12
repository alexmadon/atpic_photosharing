#!/usr/bin/python3

import atpic.daemonize
import atpic.zmq_auth_server

atpic.daemonize.start(atpic.zmq_auth_server.main_loop,'/var/run/zmq_auth.pid')
