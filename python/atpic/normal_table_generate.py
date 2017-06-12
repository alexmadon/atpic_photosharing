#!/usr/bin/python3
import re

f=open('Latin-ASCII.xml','r')
print("table={")
for line in f.readlines():
    re1=re.compile('<tRule>(.+)→(.+); #.*')
    if re1.search(line):
        # print('line=',line)
        a=re1.search(line)
        a1=a.group(1)
        a2=a.group(2)
        a11=a1.strip()
        a22=a2.strip()
        a22=a22.strip("'")
        # print(a11)
        # print(a22)
        print("   '",a11,"':'",a22,"',",sep="")
    else:
        pass
print("}")
