#!/usr/bin/python3
import time

if __name__ == "__main__":
    
    start = time.clock()
    for i in range(1000):
        f=open('/atpicdns/alex','rb')

        a=f.read()
        f.close()
        # print('a=',a)
    elapsed = time.clock() - start
    print(elapsed)
