#!/usr/bin/python3
# re.match('[ก-๛]','แล้วพบกันใหม่')
# http://answers.oreilly.com/topic/215-how-to-use-unicode-code-points-properties-blocks-and-scripts-in-regular-expressions/

# U+0E00…U+0E7F    \p{InThai}
import re

# U+3040…U+309F	\p{InHiragana}
# U+30A0…U+30FF	\p{InKatakana}
def detect(ss):
    sse=ss.decode('utf8')
    RE=re.compile('[\u3040-\u309F\u30A0-\u30FF]')
    if RE.search(sse):
        return True
    else:
        return False

if __name__ == "__main__":
    alist=[
        'インデックスに',
        'インデックスに alex',
        '食べました', # hiragana
        'aべました', # hiragana
        'コーヒー', # kōhī, katakana
        'alex',
        ]
    for s in alist:
        res=detect(s.encode('utf8'))
        print(s,res)


