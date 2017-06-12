#!/usr/bin/python3
# http://stackoverflow.com/questions/2718196/find-all-chinese-text-in-a-string-using-python-and-regex

# The short, but relatively comprehensive answer for narrow Unicode builds of python (excluding ordinals > 65535 which can only be represented in narrow Unicode builds via surrogate pairs):

# RE = re.compile(u'[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]', re.UNICODE)
# nochinese = RE.sub('', mystring)

# The code for building the RE, and if you need to detect Chinese characters in the supplementary plane for wide builds:

# -*- coding: utf-8 -*-
# import re

# LHan = [[0x2E80, 0x2E99],    # Han # So  [26] CJK RADICAL REPEAT, CJK RADICAL RAP
#         [0x2E9B, 0x2EF3],    # Han # So  [89] CJK RADICAL CHOKE, CJK RADICAL C-SIMPLIFIED TURTLE
#         [0x2F00, 0x2FD5],    # Han # So [214] KANGXI RADICAL ONE, KANGXI RADICAL FLUTE
#         0x3005,              # Han # Lm       IDEOGRAPHIC ITERATION MARK
#         0x3007,              # Han # Nl       IDEOGRAPHIC NUMBER ZERO
#         [0x3021, 0x3029],    # Han # Nl   [9] HANGZHOU NUMERAL ONE, HANGZHOU NUMERAL NINE
#         [0x3038, 0x303A],    # Han # Nl   [3] HANGZHOU NUMERAL TEN, HANGZHOU NUMERAL THIRTY
#         0x303B,              # Han # Lm       VERTICAL IDEOGRAPHIC ITERATION MARK
#         [0x3400, 0x4DB5],    # Han # Lo [6582] CJK UNIFIED IDEOGRAPH-3400, CJK UNIFIED IDEOGRAPH-4DB5
#         [0x4E00, 0x9FC3],    # Han # Lo [20932] CJK UNIFIED IDEOGRAPH-4E00, CJK UNIFIED IDEOGRAPH-9FC3
#         [0xF900, 0xFA2D],    # Han # Lo [302] CJK COMPATIBILITY IDEOGRAPH-F900, CJK COMPATIBILITY IDEOGRAPH-FA2D
#         [0xFA30, 0xFA6A],    # Han # Lo  [59] CJK COMPATIBILITY IDEOGRAPH-FA30, CJK COMPATIBILITY IDEOGRAPH-FA6A
#         [0xFA70, 0xFAD9],    # Han # Lo [106] CJK COMPATIBILITY IDEOGRAPH-FA70, CJK COMPATIBILITY IDEOGRAPH-FAD9
#         [0x20000, 0x2A6D6],  # Han # Lo [42711] CJK UNIFIED IDEOGRAPH-20000, CJK UNIFIED IDEOGRAPH-2A6D6
#         [0x2F800, 0x2FA1D]]  # Han # Lo [542] CJK COMPATIBILITY IDEOGRAPH-2F800, CJK COMPATIBILITY IDEOGRAPH-2FA1D
# 
# def build_re():
#     L = []
#     for i in LHan:
#         if isinstance(i, list):
#             f, t = i
#             try: 
#                 f = unichr(f)
#                 t = unichr(t)
#                 L.append('%s-%s' % (f, t))
#             except: 
#                 pass # A narrow python build, so can't use chars > 65535 without surrogate pairs!
# 
#         else:
#             try:
#                 L.append(unichr(i))
#             except:
#                 pass
# 
#     RE = '[%s]' % ''.join(L)
#     print 'RE:', RE.encode('utf-8')
#     return re.compile(RE, re.UNICODE)
# 
# RE = build_re()
# print RE.sub('', u'美国').encode('utf-8')
# print RE.sub('', u'blah').encode('utf-8')
# 

import re
def detect(ss):
    """
    Returns True if the input bytes conbtain chinese
    """
    sse=ss.decode('utf8')
    RE = re.compile('[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]')
    if RE.search(sse):
        return True
    else:
        return False

if __name__ == "__main__":
    alist=['个性化首页 · 网络历史记录','alex','alex 个性化首页 · 网络历史记录']
    for s in alist:
        res=detect(s.encode('utf8'))
        print(s,res)
