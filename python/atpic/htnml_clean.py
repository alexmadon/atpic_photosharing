# see also http://code.activestate.com/recipes/52281/

11.7 Stripping Dangerous Tags and Javascript from HTML
Credit: Itamar Shtull-Trauring
11.7.1 Problem
You have received some HTML input from a user and need to make sure that the HTML is clean.
You want to allow only safe tags, to ensure that tags needing closure are indeed closed, and,
ideally, to strip out any Javascript that might be part of the page.
11.7.2 Solution
The sgmllib module helps with cleaning up the HTML tags, but we still have to fight against
the Javascript:
import sgmllib, string
class StrippingParser(sgmllib.SGMLParser):
       # These are the HTML tags that we will leave intact
       valid_tags = ('b', 'a', 'i', 'br', 'p')
       tolerate_missing_closing_tags = ('br', 'p')
       from htmlentitydefs import entitydefs # replace
entitydefs from sgmllib
       def _ _init_ _(self):
               sgmllib.SGMLParser._ _init_ _(self)
               self.result = []
               self.endTagList = []
       def handle_data(self, data):
               self.result.append(data)
       def handle_charref(self, name):
               self.result.append("&#%s;" % name)
       def handle_entityref(self, name):
               x = ';' * self.entitydefs.has_key(name)
               self.result.append("&%s%s" % (name, x))
       def unknown_starttag(self, tag, attrs):
               """ Delete all tags except for legal ones. """
               if tag in self.valid_tags:
                      self.result.append('<' + tag)
                      for k, v in attrs:
                            if string.lower(k[0:2]) != 'on' and
string.lower(
                                          v[0:10]) != 'javascript':
                                   self.result.append(' %s="%s"' % (k, v))
                      self.result.append('>')
                      if tag not in self.tolerate_missing_closing_tags:
                            endTag = '</%s>' % tag
                            self.endTagList.insert(0,endTag)
    def unknown_endtag(self, tag):
        if tag in self.valid_tags:
            # We don't ensure proper nesting of
opening/closing tags
            endTag = '</%s>' % tag
            self.result.append(endTag)
            self.endTagList.remove(endTag)
    def cleanup(self):
        """ Append missing closing tags. """
        self.result.extend(self.endTagList)
def strip(s):
    """ Strip unsafe HTML tags and Javascript from string s.
"""
    parser = StrippingParser( )
    parser.feed(s)
    parser.close( )
    parser.cleanup( )
    return ''.join(parser.result)
