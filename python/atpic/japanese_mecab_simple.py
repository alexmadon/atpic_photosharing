#!/usr/bin/python3

from ctypes import *
from ctypes.util import find_library

# WARNING!!!!!!!
# mecab needs to have the UTF8 dictionaries!!!!!!
# test with command line


# https://github.com/sinsai/message_naive_bayes_classifier/blob/master/mecab.py
# http://coderepos.org/share/browser/lang/python/hama/src/hama_wordstat.py
# javascript ctypes?????
# http://code.google.com/p/itadaki/source/browse/trunk/content/my_worker.js
# https://gist.github.com/728118 **** Japanese speech engine wrapper for Open JTalk (part of NVDAjp)

# python ctypesgen.py -lneon /usr/local/include/neon/ne_*.h -o neon.py
# -lmecab /usr/include/mecab.h
# ./ctypesgen.py -lmecab /usr/include/mecab.h -o mecab.py
def sparse_all(s):
	# ライブラリの場所を指定
	# ライブラリを ctypes を使って読み込み
	mecabpath = find_library('mecab')

	lib = cdll.LoadLibrary(mecabpath)
	# lib = CDLL(find_library("iconv"), RTLD_GLOBAL) 
	# 解析器初期化用の引数を指定（第二引数無しで普通の解析)
	argc = c_int(2)
	argv = (c_char_p * 2)(b"mecab", b"")

	# 解析器のオブジェクトを作る
	# mecab_t*      mecab_new(int argc, char **argv);

	tagger = lib.mecab_new(argc, argv)

	print(tagger)
	""" 指定された文字列を品詞など調べて返す。 """

	# const char*   mecab_sparse_tostr(mecab_t *mecab, const char *str);

	s = lib.mecab_sparse_tostr(tagger, s)
	ret = c_char_p(s).value

	# 終わったら、一応、殺しておく 
	lib.mecab_destroy(tagger)
	return ret

"""
テスト内容
sparse_all("本日は晴天なり")
>> 本日 は 晴天 なり
"""

if __name__ == "__main__":
	# input="本日は晴天なり".encode('utf8')
	input="alex madon"
	res=sparse_all(input)
	print(res)
	print(res.decode('utf8'))
