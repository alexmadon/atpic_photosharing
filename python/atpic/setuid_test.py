import os

os.setuid(33)
f=open("/tmp/test1","w")
f.write("alex")
f.close()
