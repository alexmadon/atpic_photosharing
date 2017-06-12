#!/usr/bin/python3
# apt-get install libthai0 libthai-doc libthai-dev libthai-data
# th_brk libthai
# file:///usr/share/doc/libthai-doc/html/thbrk_8h.html
# 
# file:///usr/share/doc/libthai-doc/html/thwbrk_8h.html
# file:///usr/share/doc/libthai-doc/html/thwchar_8h.html
# 
# int th_wbrk_line 	( 	const thwchar_t *  	in,
# 		thwchar_t *  	out,
# 		size_t  	n,
# 		const thwchar_t *  	delim 
# 	) 

# h2xml
# xml2py
# /usr/include/thai
# /usr/include/thai/thailib.h
# h2xml -I /usr/include/thai /usr/include/thai/thbrk.h -o thailib.xml
# xml2py  thailib.xml -k f -o  thailib.py
from ctypes import *
from ctypes.util import find_library

THAI_LIBRARY = find_library('thai')
if not THAI_LIBRARY:
    raise OSError('Cannot find libthai in the system')
# libya
thai = cdll.LoadLibrary(THAI_LIBRARY)

print(thai)


thchar_t = c_ubyte
# int th_wbrk(const thwchar_t *s, int pos[], size_t n);

# typedef wchar_t thwchar_t;

# int th_wbrk_line(const thwchar_t *in, thwchar_t *out, size_t n, const thwchar_t *delim);
# int th_wbrk_line 	( 	const thwchar_t *  	in,
# 		thwchar_t *  	out,
# 		size_t  	n,
# 		const thwchar_t *  	delim 
#	)
# Parameters
#     in	: the input wide-char string to be processed
#     out	: the output wide-char buffer
#     n	: the size of out (as number of elements)
#     delim	: the wide-char word delimitor to insert
# Returns:
# the actual size of the processed string (as number of elements) 

thai.th_wbrk_line.restype = c_int
thai.th_wbrk_line.argtypes = [c_wchar_p,c_wchar_p,c_size_t,c_wchar_p]
# wchar_t

# print(thai.th_wbrk_line)

def whitespace(ain):
    # expects bytes
    ain=ain.decode('utf8')
    aout=whitespace_string(ain)
    return aout.encode('utf8')

def whitespace_string(ain):
    # expects a string
    # ain='แล้วพบกันใหม่'
    aout=' '*(2*len(ain)+1) 
    # we assume that the maximum length is a set of one character + white space
    adelim=' '
    asize=len(aout)
    # http://stackoverflow.com/questions/12013599/how-to-cast-multiple-integers-as-a-ctypes-array-of-c-ubyte-in-python
    # ctypes.ArgumentError: argument 4: <class 'TypeError'>: expected LP_c_ubyte instance instead of bytes
    
    
    res=thai.th_wbrk_line(ain,aout,asize,adelim)
    print('ain',ain)
    print('len(ain)',len(ain))
    print('res',res)
    print('asize=',asize)
    print('aout=',aout,';')
    print('len(aout)=',len(aout),';')
    print('aout[:res]',aout[:res])
    result=aout[:res]
    print(dir(aout))
    return result

"""
แล้วพบกันใหม่ means 'See you later.'

and is compound by three words:

แล้ว
พบกัน
ใหม่
"""


if __name__ == "__main__":
    
    ain='แล้วพบกันใหม่'
    aout=whitespace_string(ain)
    print(ain,'=>',aout)
    aout=whitespace(ain.encode('utf8'))
    print(aout.decode('utf8'))
