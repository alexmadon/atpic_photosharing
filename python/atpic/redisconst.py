# antidos:
REDIS_IP_CNT=b'ip:' # redis IP hit counter 
REDIS_IP_BLK=b'bk:' # redis blacklisted IPs


# idbased
REDIS_ID_UPART=b'pt:' # redis partition for this uid
REDIS_ID_GPERM=b'gp:' # redis gallery permission for this gid

# pathbased PatH

REDIS_PH_UNODE=b'un:' # redis uid,partition for this dns uname
REDIS_PH_GNODE=b'gn:' # redis g stats for this uid,gpath
REDIS_PH_PNODE=b'pn:' # redis p stats for this gid,ppath

# wurfl user agent WurFl
REDIS_WF_UA=b'ua:' # redis wurfl user agent

# redis captcha
REDIS_CAPTCHA=b'ca:' # redis wurfl user agent

# stats
REDIS_STATS=b'st:' # redis stats

# index
REDIS_INDEX=b'ix:' # indexing queue
