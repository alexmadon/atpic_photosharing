#!/usr/bin/python3

import atpic.daemonize
import atpic.zmq_asyncpro_server

atpic.daemonize.start(atpic.zmq_asyncpro_server.main_loop,'/var/run/zmq_asyncpro.pid')
