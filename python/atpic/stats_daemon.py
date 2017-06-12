#!/usr/bin/python3

import atpic.log
import atpic.redis_pie
import atpic.stats
xx=atpic.log.setmod("INFO","stats_daemon")

if __name__ == "__main__":
    rediscon=atpic.redis_pie.Redis()
    atpic.stats.daemon(rediscon)
