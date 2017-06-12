#!/usr/bin/python3

# http://answers.oreilly.com/topic/215-how-to-use-unicode-code-points-properties-blocks-and-scripts-in-regular-expressions/
# U+2000…U+206F	\p{InGeneral_Punctuation}
# U+3000…U+303F	\p{InCJK_Symbols_and_Punctuation}

import re

def replacewithwhitespace(ss):
    sse=ss.decode('utf8')
    RE=re.compile('[ \?\!\,\.\[\]\{\}\-\_\=\+\(\)\*\&\^\%\$\£\"\!\`\`\';\:\#\~\|\<\>\u2000-\u206F\u3000-\u303F·]+')
    ssr=RE.sub(' ',sse)
    return ssr.encode('utf8')

if __name__ == "__main__":
    alist=[
        'Hello!!!?,alex',
        '个性化首页 · 网络历史记录'
        ]
    for s in alist:
        res=replacewithwhitespace(s.encode('utf8'))
        print(s,res.decode('utf8'))

