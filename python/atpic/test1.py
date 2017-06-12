#!/usr/bin/python3
import atpic.log


# import logging

import atpic.dispatcher
import atpic.log
import atpic.redis_pie
from atpic.redisconst import *
import atpic.mybytes


xx=atpic.log.setmod("INFO","test1")


def hi():
    yy=atpic.log.setname(xx,'hi')
    atpic.log.debug(yy,'starting...')

if __name__ == "__main__":
    rediscon=atpic.redis_pie.Redis()
    hi()
