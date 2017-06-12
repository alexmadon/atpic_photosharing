from ctypes.util import find_library

# mecabpath = find_library('mecab')
# find_library("iconv")
# find_library('fuse')
# find_library('pq')

for library in ['mecab','iconv','fuse','pq']:
    path=find_library(library)
    print(library,'->',path)
    if not path:
        raise Exception('library not found')
