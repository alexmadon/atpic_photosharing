#!/usr/bin/python3

import atpic.log

xx=atpic.log.setmod("INFO","wikinormalizer")

"""
Used to normalize the wiki URLs
we lowercase,
replace white spaces with underscore _

This is important as this the key that is used to store/retrieve wiki pages.
"""

# may need a permanent redirect to avoid ronts indexing several times one page
import atpic.normal

def normalize(s):
    s=atpic.normal.remove_diacritics(s)
    s=s.lower()
    s=s.replace(b' ',b'_')
    return s

if __name__ == "__main__":
    print('hi')
    inputs=(
        b'FTP',
        b'File Upload',
        b'go-go',
        b'Europe/France'
        )

    for s in inputs:
        n=normalize(s)
        print(s,'->',n)
