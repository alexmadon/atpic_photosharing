#!/usr/bin/python3
# use unicode data and categories
# http://www.fileformat.info/info/unicode/category/index.htm
import re
import unicodedata
import atpic.normal_table

# import unidecode # http://stackoverflow.com/questions/12944678/using-unicodedata-normalize-in-python-2-7

import codecs # http://stackoverflow.com/questions/1382998/latin-1-to-ascii
# http://en.wikipedia.org/wiki/Combining_character

# http://unicode.org/charts/PDF/U0300.pdf 
# Combining Diacritical Marks
# Range: 0300­036F


# http://stackoverflow.com/questions/115210/utf-8-validation
# >>> b='\xce\xb3\xce\xb5\xce\xb9\xff\xb1' # note second-to-last char changed
# >>> print b.decode("utf_8")
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/usr/local/lib/python2.5/encodings/utf_8.py", line 16, in decode
#     return codecs.utf_8_decode(input, errors, True)
# UnicodeDecodeError: 'utf8' codec can't decode byte 0xff in position 6: unexpected code byte

# http://unicode.org/charts//PDF/Unicode-5.2/U52-1DC0.pdf
# Combining Diacritical Marks Supplement
# Range: 1DC0­1DFF

# http://unicode.org/charts/PDF/U32-20D0.pdf 
# Combining Diacritical Marks for Symbols Range
# Range: 20D0–20FF

# http://unicode.org/charts/PDF/UFE20.pdf
# Combining Half Marks
# Range: FE20­FE2F


# character fallback
# http://stackoverflow.com/questions/12944678/using-unicodedata-normalize-in-python-2-7
# http://unicode.org/repos/cldr/trunk/common/transforms/Latin-ASCII.xml
# œ -> oe

# cat Latin-ASCII.xml |perl -pi -e "s/<tRule>(.+) → (.+) ;.*/XX'\1':\2,/g"| grep  XX| perl -pi -e "s/.*XX//" > tt
def transtable():
    ttable=atpic.normal_table.table
    ttrans=str.maketrans(ttable)
    return ttrans


def whatcategorie():
    keys=atpic.normal_table.table.keys()
    keys=list(keys)
    keys.sort()
    for c in keys:
         print(c,unicodedata.category(c),unicodedata.name(c))

def strip_OLD(text):
    # in arabic
    # http://www.techques.com/question/1-5224267/javascript+remove-arabic-text-diacritic-dynamically
    return ''.join([c for c in unicodedata.normalize('NFD', text) \
        if unicodedata.category(c) != 'Mn'])

def strip(text):
    out=[]

    for c in unicodedata.normalize('NFD', text):
        # print('----------')
        # print(c,'=categ:',unicodedata.category(c))
        # http://www.fileformat.info/info/unicode/category/index.htm
        # print(c,'=name:',unicodedata.name(c))
        categ= unicodedata.category(c)
        if categ in ['Mn','Lm']:
            # ARABIC TATWEEL is in 'Lm'='Letter, Modifier'
            # cedilla in 'Mn'='Mark, Nonspacing'
            # print('dropping',unicodedata.name(c))
            pass
        elif categ[0]=='P':
            # [Pc] 	Punctuation, Connector
            # [Pd] 	Punctuation, Dash
            # [Pe] 	Punctuation, Close
            # [Pf] 	Punctuation, Final quote (may behave like Ps or Pe depending on usage)
            # [Pi] 	Punctuation, Initial quote (may behave like Ps or Pe depending on usage)
            # [Po] 	Punctuation, Other
            # [Ps] 	Punctuation, Open
            out.append(' ') # replace with a white space
        else:
            out.append(c)
            pass
    s=''.join(out)
    ttrans=transtable()
    s=s.translate(ttrans)
    return s

def remove_diacritics(s):
    s=s.decode('utf8')
    norm=strip(s)
    norm=norm.encode('utf8')
    return norm

def remove_diacritics_OLD(s):
    " Decomposes string, then removes combining characters "
    # return reCombining.sub('',unicodedata.normalize('NFD',str(s)) )

    # reCombining = re.compile('[\u0300-\u036f\u1dc0-\u1dff\u20d0-\u20ff\ufe20-\ufe2f]',re.U)
    reCombining = re.compile('[\u0300-\u036f\u1dc0-\u1dff\u20d0-\u20ff\ufe20-\ufe2f]')
    # Java: reCombining =re.compile("\p{InCombiningDiacriticalMarks}+")


    s=s.decode('utf8')
    norm=reCombining.sub('',unicodedata.normalize('NFD',s) )
    norm=norm.encode('utf8')
    return norm

if __name__ == "__main__":
    # http://stackoverflow.com/questions/12391348/combined-diacritics-do-not-normalize-with-unicodedata-normalize-python

    # arabic http://packages.python.org/Tashaphyne/Tashaphyne.normalize-module.html
    # http://nullege.com/codes/search/Support.ar_ctype.strip_tashkeel
    # http://packages.python.org/PyArabic/pyarabic.araby-module.html
    # >>> text=u"الْعَرَبِيّةُ"
    # >>> stripTashkeel(text)
    # العربية
    # https://github.com/Alfanous-team/alfanous/blob/master/src/alfanous/Support/ar_ctype.py
    # http://www.techques.com/question/1-5224267/javascript+remove-arabic-text-diacritic-dynamically

    tester=["cet été là","Garçon","أهلاً بِكْ","bœuf","schluß"] # arabic
    for s in tester:
        out=remove_diacritics(s.encode('utf8'))
        print(s,'=>',out.decode('utf8'))
        print()
        print(s,'++>',strip(s))
        print()
        # print(remove_diacritics(s))

    whatcategorie()
