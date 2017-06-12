#!/usr/bin/python3
# this reduces (removes HTML tags, covert to text)
# normalize (remove accents, cedillas etc...)
# lowercase
# and separate words (thai, chinese, japanese) using a white space
import time

import atpic.cleaner
import atpic.normal
# import atpic.punctuation # not used anymore: use normal

import atpic.thai_detect
import atpic.thai_libthai

import atpic.japanese_detect
import atpic.japanese_mecab # tokenizer
import atpic.japanese_tinysegmenter # another simpler tokenizer

import atpic.chinese_detect
import atpic.chinese_adso # tokenizer
import atpic.chinese_charspace # another simpler tokenizer

import atpic.log
xx=atpic.log.setmod("INFO","tokenizer")

def tokenize(ss):

    """
    Returns a string with spaces between words and all HTML tags removed
    """
    yy=atpic.log.setname(xx,'tokenize')
    # do not apply adso on Japanese as there is a bug
    atpic.log.debug(yy,'input=',ss)

    if atpic.japanese_detect.detect(ss):
        atpic.log.debug(yy,'there is some japanese')
        ss=atpic.japanese_mecab.whitespace(ss)
        # ss=atpic.japanese_tinysegmenter.whitespace(ss)
    elif atpic.chinese_detect.detect(ss):
        atpic.log.debug(yy,'there is some chineese')
        ss=atpic.chinese_charspace.whitespace(ss)
    if atpic.thai_detect.detect(ss):
        atpic.log.debug(yy,'there is some thai')
        ss=atpic.thai_libthai.whitespace(ss)

    atpic.log.debug(yy,'after asian',ss)
    ss=atpic.normal.remove_diacritics(ss)
    atpic.log.debug(yy,'afternormal',ss)
    ss=atpic.cleaner.txt(ss)
    atpic.log.debug(yy,'after clean',ss)
    ss=ss.lower()
    # ss=atpic.punctuation.replacewithwhitespace(ss)
    ss=ss.strip()
    return ss


if __name__ == "__main__":
    alist=['个性化首页 · 网络历史记录','alex','alex 个性化首页 · 网络历史记录',"cet été là","Garçon","แล้วพบกันใหม่","私の名前は中野です","alex madon 本日は晴天なり","HELLO!!?. My dear!",'<a href="http://google.com">my site</a>']
    i=0
    for s in alist:
        i=i+1
        print('============',i,'==============')
        print(s)
        start = time.clock()
        res=tokenize(s.encode('utf8'))
        elapsed = time.clock() - start
        print('took:',elapsed)
        print(res.decode('utf8'))
        print('XXX ("',s,'","',res.decode('utf8'),'"),',sep='')
