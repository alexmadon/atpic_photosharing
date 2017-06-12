#!/usr/bin/python3
import re


import atpic.environment
import atpic.log
import atpic.mybytes


xx=atpic.log.setmod("INFO","wiki_lines")

def get_lines(environ):
    # used to match query_string lines for wiki zone edit
    lines=atpic.environment.get_qs_key(environ,b'lines',b"")
    res=False
    if lines:
        match=re.match(b'^([0-9]+)-([0-9]+)$',lines)
        if match:
            res=(match.group(1),match.group(2))
    return res


def extract(text,line_from,line_to):
    lines=text.splitlines()
    print(lines)
    fromb=atpic.mybytes.bytes2int(line_from)
    tob=atpic.mybytes.bytes2int(line_to)
    zone=lines[fromb-1:tob]
    zonest=b'\n'.join(zone)
    return zonest

def replace(wikitext,wikilines,line_from,line_to):
    wikitext_lines=wikitext.splitlines()
    wikilines_lines=wikilines.splitlines()
    fromb=atpic.mybytes.bytes2int(line_from)
    tob=atpic.mybytes.bytes2int(line_to)
    newwikitext_lines=wikitext_lines[:fromb-1]+wikilines_lines[:]+wikitext_lines[tob:]
    newwikitext=b'\n'.join(newwikitext_lines)
    return newwikitext

if __name__ == "__main__":
    lines=get_lines({b'QUERY_STRING':b'lines=10-13',})
    print(lines)
    zone=extract(b'one\ntwo,\nthree\nfour',b'1',b'3')
    print(zone)


