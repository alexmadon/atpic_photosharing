#!/usr/bin/python3

langs=['en']

out=open('translationspy.py','w')
out.write('#!/usr/bin/python3')

print(file=out)
print(file=out)
print("# automatically generated with maketramslations.py",file=out)
print("# DO NOT EDIT",file=out)
print(file=out)
print("trans={}",file=out)

for lang in langs:
    fname='translations/'+lang+'.properties'
    print("processing ...",fname)
    f=open(fname)
    lang=lang.encode('utf8')
    print("trans[",lang,"]={}",sep='',file=out)


    for line in f:
        # print('aline',line)
        line=line.strip()
        splitted=line.split('=')
        key=splitted[0]
        phrase='='.join(splitted[1:])
        key=key.encode('utf8')
        phrase=phrase.encode('utf8')
        print("trans[",lang,"][",key,"]=",phrase,sep='',file=out)



out.close()
f.close()
print("Done")
