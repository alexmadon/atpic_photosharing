#!/usr/bin/python3
def fun1(callback):
    for i in range(1,10):
        callback(i)

def fun2(i):
    print(i)


# now a callback with arguments

def funarg1(callback,*args):
    for i in range(1,10):
        callback(i,*args)

    
def funarg2(i,k,m):
    print(i,k,m)

if __name__=="__main__":
    fun1(fun2)
    funarg1(funarg2,4,10)
