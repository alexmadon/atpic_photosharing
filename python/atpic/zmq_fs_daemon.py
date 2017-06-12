#!/usr/bin/python3

import atpic.daemonize
import atpic.zmq_fs_server

atpic.daemonize.start(atpic.zmq_fs_server.main_loop,'/var/run/zmq_fs.pid')
