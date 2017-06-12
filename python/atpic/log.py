#!/usr/bin/python3
from atpic.prunt import prunt
import syslog

# syslog.syslog(syslog.LOG_DEBUG, 'heeeloooo')
# http://www.rsyslog.com/tag/rate-limiting/
# $SystemLogRateLimitInterval [number]
# $SystemLogRateLimitBurst [number]

# The SystemLogRateLimitInterval determines the amount of time that is being measured for rate limiting. By default this is set to 5 seconds. The SystemLogRateLimitBurst defines the amount of messages, that have to occur in the time limit of SystemLogRateLimitInterval, to trigger rate limiting. Here, the default is 200 messages. For creating a more effective test, we will alter the default values.
# at the start of each file:
# import atpic.log
# xx=atpic.log.setmod("xmlutils")
# and at start of each function:
#     yy=atpic.log.setname(xx,"rec_send")
#     atpic.log.debug(yy,'receied',message)

# you can control with the first element:
# ERROR, INFO, DEBUG, simply string based
# can then debug one module only or one function only

def setmod(*args): # at module level
    return ' '.join(args)

def setname(*args): # at function level
    return '.'.join(args) # 'atpic.'+prefix+'.'+name+':'


# now the output at the various levels

def debug(*args, sep=' ', end=''):
    if args[0].startswith('DEBUG'):
        # DEBUG
        syslog.syslog(syslog.LOG_DEBUG, prunt(*args, sep=sep, end=end,level='DEBUG'))
    else:
        # ERROR WARN INFO
        pass

def info(*args, sep=' ', end=''):
    if args[0].startswith('ERROR') or  args[0].startswith('WARN') :
        # ERROR WARN
        pass
    else:
        # INFO DEBUG
        syslog.syslog(syslog.LOG_DEBUG, prunt(*args, sep=sep, end=end, level='INFO'))

def warn(*args, sep=' ', end=''):
    # warn is logged in all levels, except if only interested in errors
    if args[0].startswith('ERROR'):
        # ERROR
        pass
    else:
        # WARN INFO DEBUG
        syslog.syslog(syslog.LOG_DEBUG, prunt(*args, sep=sep, end=end, level='WARN'))

def error(*args, sep=' ', end=''):
    # error is logged whatever the log level
    # ERROR WARN INFO DEBUG
    syslog.syslog(syslog.LOG_DEBUG, prunt(*args, sep=sep, end=end,level='ERROR'))


if __name__ == "__main__":
    print("check you /var/log/user.log")
    info("Testing logging")
