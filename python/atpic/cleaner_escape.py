# py3k version

# import htmllib
import html

# def unescape2(s):
#     p = htmllib.HTMLParser(None)
#     p.save_bgn()
#     p.feed(s)
#     return p.save_end()


def unescape(s):
    s = s.replace(b"&quot;", b'"')
    s = s.replace(b"&lt;", b"<")
    s = s.replace(b"&gt;", b">")
    # this has to be last:
    s = s.replace(b"&amp;", b"&")
    return s


def escape(input):
    input=input.decode('utf8')
    input=html.escape(input)
    input=input.encode('utf8')
    input=input.replace(b'"', b"&quot;") # due to problems in json
    return input
