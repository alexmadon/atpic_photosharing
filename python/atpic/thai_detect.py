#!/usr/bin/python3
# re.match('[ก-๛]','แล้วพบกันใหม่')
# http://answers.oreilly.com/topic/215-how-to-use-unicode-code-points-properties-blocks-and-scripts-in-regular-expressions/

# U+0E00…U+0E7F    \p{InThai}
import re

def detect(ss):
    sse=ss.decode('utf8')
    RE=re.compile('[\u0E00-\u0E7F]')
    if RE.search(sse):
        return True
    else:
        return False

if __name__ == "__main__":
    alist=['แล้วพบกันใหม่','alex','alex แล้วพบกันใหม่']
    for s in alist:
        res=detect(s.encode('utf8'))
        print(s,res)


