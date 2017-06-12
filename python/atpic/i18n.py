#!/usr/bin/python3
# used in xslt
#  to achieve i18n
# features:
# parameter substitution
import re


import atpic.translationspy


trans=atpic.translationspy.trans

# http://legacy.python.org/dev/peps/pep-3101/
def prant(*args):
    print('++++++++++++++++++')
    print(*args)
    print(args[0],args[1:])
    try:
        print(args[0].format(*args[1:]))
    except:
        print(args[0])


def translate(lang,key):
    try:
        s=trans[lang][key]
    except:
        try:
            s=trans[b'en'][key]
        except:
            s=b'MISSING'+key
    return s

def parse(*args):
    lang=args[0] # eg 'en'
    key=args[1] # eg "authenticatedas"
    values=args[2:]

    # lookup a translation based on lang+key
    s=translate(lang,key)
    res=replace(s,values)
    return res

def replace(s,values):
    pattern=re.compile(b'{([0-9]+)}')
    iterator=pattern.finditer(s)
    # values=[b'alex',b'France']
    res=[]
    ifrom=0
    for match in iterator:
        print(match)
        print(match.group())
        print(match.group(1))
        print(match.span())
        sp=match.span()
        ito=sp[0]
        if s[ifrom:ito]:
            res.append(b'<xsl:text>')
            res.append(s[ifrom:ito])
            res.append(b'</xsl:text>')
        ifrom=sp[1]
        pos=int(match.group(1))
        print(values[pos])
        res.append(values[pos])

    if s[ifrom:]:
        res.append(b'<xsl:text>')
        res.append(s[ifrom:])
        res.append(b'</xsl:text>')
    res=b''.join(res)
    print(res)
    return res

if __name__ == "__main__":
    print('hi')

    replace(b'authenticated as {0} from {1}!',[b'Alex',b'France'])
    replace(b'authenticated as {0} from {1}',[b'Alex',b'France'])

    parse(b'en',b'logout')
    parse(b'en',b'authenticatedas',b'Alex')

