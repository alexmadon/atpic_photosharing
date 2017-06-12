#!/usr/bin/python3.1
"""
This generates a python file that just dumps the XML mnodel file to a python string.
"""

f=open('tt.xml','r')
xmls=f.read()
f.close()

s=list()
s.append('def getmodel():')
s.append('\ts="""%s"""' % xmls)
s.append('\treturn s')
ss='\n'.join(s)


f=open('model_pystring.py','w')
f.write(ss)
f.close()
