#!/usr/bin/python3

# apt-get install python3-docutils

# $Id: rst2html.py 4564 2006-05-21 20:44:42Z wiemann $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
A minimal front end to the Docutils Publisher, producing HTML.
"""

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description


# http://pastebin.com/isRzAatW
# #112  -> http://mytracsite/tickets/112
# r1023 -> http://mytracsite/changeset/1023
 
from docutils import nodes, utils
from docutils.parsers.rst import roles
import urllib

import sys

trac_url = 'http://mytratsite/'

def trac2_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
  ref = trac_url + 'intertrac/' + text # urllib.quote(text, safe='')
  node = nodes.reference(rawtext, utils.unescape(text), refuri=ref, **options)
  return [node],[]

# def trac_role(
def trac_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    print('checkink',(name, rawtext, text, lineno, inliner,options,content),file=sys.stderr)
    myuri='http://mysite.com/'+text+'||'+rawtext
    reference = nodes.reference(rawtext, text,refuri=myuri)
    return [reference], []



roles.register_canonical_role('trac', trac_role)

roles.DEFAULT_INTERPRETED_ROLE = 'trac'



description = ('Generates (X)HTML documents from standalone reStructuredText '
               'sources.  ' + default_description)

publish_cmdline(writer_name='html', description=description)
