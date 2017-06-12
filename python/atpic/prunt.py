#!/usr/bin/python3
# in py3k, print signature is: def print(*args, sep=' ', end='\n', file=None)
# http://stackoverflow.com/questions/812422/why-does-python-logging-package-not-support-printing-variable-length-args
import io
import os
import threading

def prunt(*args, sep=' ', end='', level='DEBUG'):
    output = io.StringIO()
    print(str(os.getpid()),end=' ',file=output)

    mypid=threading.current_thread()
    print(mypid.name,end=' ',file=output)
    print(level,end='_',file=output)

    print(*args, sep=sep, end=end, file=output)
    contents = output.getvalue()
    output.close()
    return contents


if __name__ == "__main__":
    print('hi')
    print(prunt("alex","madon"))
    a=(1,2,3,4)
    b=b"alex madon"
    print(prunt(a,b))
