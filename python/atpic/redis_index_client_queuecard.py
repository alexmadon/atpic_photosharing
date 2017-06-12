#!/usr/bin/python3
import atpic.redis_index_client

if __name__ == "__main__":
    rediscon=atpic.redis_pie.connect_first()
    numitems=atpic.redis_index_client.get_queue_card(rediscon)
    print('number of items in index queue=',numitems)
