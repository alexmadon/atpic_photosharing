# -*- coding: utf-8 -*-
from pymmseg import mmseg

mmseg.dict_load_defaults()

text="兴奋得很晚都睡不着"

algor = mmseg.Algorithm(text)
for tok in algor:
    print '%s [%d..%d]' % (tok.text, tok.start, tok.end)

