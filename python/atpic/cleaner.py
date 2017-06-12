# from atpic.html_filter import html_filter
"""
This is a wrapper of the cleaning function:

use this package.


"""
import atpic.cleaner_alex
import atpic.cleaner_escape
import re


# import logging
import atpic.log

xx=atpic.log.setmod("INFO","cleaner_alex")





# ================================
# the main two functions:
# ================================

def txt(input):
    """Returns a valid TXT (compatible with XML)"""
    output=atpic.cleaner_alex.txtclean(input)
    return output


def html(input):
    """Returns a valid HTML/ X-HTML"""
    output=atpic.cleaner_alex.clean(input)
    return output


# ================================
# implementation details:
# ================================


def escape(input):
    """converts to a string which can be included in a XML (solr) doc
    This needs to be reversible"""
    # first correct the HTML
    output=html(input)
    # print "HTML is: %s" % output
    # then escape it
    output=atpic.cleaner_escape.escape(output)
    # print "ESCAPD is: %s" % output
    return output

def unescape(input):
    """reverts to the original (corrected) XML"""
    output=atpic.cleaner_escape.unescape(input)
    return output

def sqlescape(input):
    output=sql(escape(input))
    return output

def sqlhtml(input):
    """cleaner used to store user input in SQL HTML"""
    output=sql(html(input))
    return output


def cleanwiki(text):
    yy=atpic.log.setname(xx,'cleanwiki')
    atpic.log.debug(yy,'input',text)
    # check encoding is valid
    try:
        text=text.decode('utf8')
        text=text.encode('utf8')
    except:
        atpic.log.debug(yy,'bad encoding')

    text=text.replace(b'<',b'&lt;')
    return text
