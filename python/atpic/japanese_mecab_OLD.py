#  -*- coding:utf-8 -*-
import MeCab
sentences = ["初音ミクは俺の嫁","兴奋得很晚都睡不着 alex madon 1968"]
# try on chinese: http://blog.wensheng.com/2008/06/pymmseg-python-mmseg.html
for sentence in sentences:
    print "doing %s" % sentence
    t = MeCab.Tagger ("")
    m = t.parseToNode (sentence)
    while m:
        print m.surface, "\t", m.feature
        m = m.next
