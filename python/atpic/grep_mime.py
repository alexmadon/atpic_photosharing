"""
time grep -b  --binary-files=text 1b2cdaa65388 /tmp/atupCdDtmV
0:------------------------------1b2cdaa65388
228808861:------------------------------1b2cdaa65388
228808961:------------------------------1b2cdaa65388--

real	0m0.199s
user	0m0.128s
sys	0m0.072s
"""

import io


fp=open("/tmp/atupCdDtmV","rb")
postion=fp.seek(228808861)
print("position",postion)
for i in range(0,10): # put a limit of 10 lines per header
    line=fp.readline()
    print(line)
    if line==b'\r\n':
        eoh=fp.seek(0,io.SEEK_CUR)
        print("END of header at",eoh)
        break
fp.close()



# http://code.activestate.com/recipes/577069-access-grep-from-python/
import subprocess

def grep(filename, arg):
    process = subprocess.Popen(['grep', '-n', arg, filename], stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr
