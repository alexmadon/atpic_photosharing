from multiprocessing import Process, Lock

def f(l, i):
    l.acquire()
    for j in range(0,100000):
        print (i,end="")
    print ()
    l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        Process(target=f, args=(lock, num)).start()
