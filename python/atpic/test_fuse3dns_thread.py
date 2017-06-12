#!/usr/bin/python3
import time
import threading
import os
from multiprocessing import Process, Lock, Queue
"""
def g():
    for i in range(10):
        f=open('/atpicdns/alex','rb')

        a=f.read()
        f.close()
        # print('a=',a)

def f(queue):
    mypid=threading.current_thread()
    print(mypid)
    pid = os.getpid()
    print(pid)
    queue.put()

if __name__ == "__main__":
    
    start = time.clock()
    queue = Queue()
    for num in range(10):

        p = Process(target=f, args=(queue,))
        p.start()

    elapsed = time.clock() - start
    print(elapsed)
"""

from multiprocessing import Process, Queue,JoinableQueue 
def g():
    print('hi')
    time.sleep(3)
    return 1

def f(q):
    q.put(g())

if __name__ == '__main__':
    # q = Queue()
    q=JoinableQueue()
    mmax=10
    start = time.clock()
    for i in range(1,mmax):
        p = Process(target=f, args=(q,))
        p.start()
        
    for i in range(1,mmax):
        print(q.get())
        # print(q.get())    # prints "[42, None, 'hello']"
        # p.join()


    # q.join()
    print('hi')
    elapsed = time.clock() - start
    print(elapsed)
