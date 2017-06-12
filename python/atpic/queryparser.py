#!/usr/bin/python3
# python3.1 version
# uses pyparsing
# we need it because in Solr we only store, uid
# if query uses uname, then we need to intercept it
# resolve the uname into uid
# and then relay to lower layer (solr)

# we also need it to intercept Chinese and insert spaces
# thai segmenter: swath
# swath - Thai word segmentation program
# langauges with no white spaces between the words of a sentence:
# chinese, japanese, thai, korean
# japanese: tinysegmenter, chasen, mecab
# chinese segmeter: good but heavy: adso
# also it allows to loose couple the search layer:
# can switch from solr to hbase
# can restrict the search to solr to some of  the fields

# from pyparsing import OneOrMore, Word, printables, dblQuotedString, removeQuotes

"""
This query parser is just the first part
A second query parsing is done to adapt the valus to the elactisearch index
like whietspace tokenizer, lower case, and ranges

"""

from pyparsing import *
import re
import atpic.log
import atpic.tokenizer
import atpic.mybytes

xx=atpic.log.setmod("INFO","queryparser")

# http://rephrase.net/days/07/04/pyparsing
# http://crpppc19.epfl.ch/doc/python-pyparsing/htmldoc/frames.html

# =============================================================
# 
#                       FIRST PARSING
#
# =============================================================
# this splits into a list of ['+','word','literal'] 


def parse_first(query):
    """
    Uses pyparsing with grammar

    this splits into a list of ['+','word','literal'] 

    """

    yy=atpic.log.setname(xx,'parse')
    atpic.log.debug(yy,'input',query)
    query=query.decode('utf8')
    # print(query)

    sign=oneOf('+ -')
    modifier=Combine(oneOf("uid gid pid Type type Licence licence f aperture exposuretime speed price lat lon make model date Filetype filetype filename username dns tree vtree treepath vtreepath path vpath bbox coord sort orderby packedcoord geopath geopackpath geopathexact geo geopack geoexact blog blogpath") + Literal(":").suppress() ) # geopath
    # aword=Regex(r"[^ ]+", re.UNICODE) # non-space chars
    aword=Regex("[^ ]+") # non-space chars
    literal=dblQuotedString | aword
    term=Group(Optional(sign,"+")+Optional(modifier,"word")+literal) # default "+word"
    expr=OneOrMore(term)

    # now we can continue simplfying (normalize)
    # literal.setParseAction(removeQuotes)
    dblQuotedString.setParseAction(removeQuotes)

    result=expr.parseString(query)
    # print(result)

    newres=myencode(result)
    atpic.log.debug(yy,'output=',newres)
    return newres

def mydecode(result):
    return mycode(result,method='decode')

def myencode(result):
    return mycode(result,method='encode')

def mycode(result,method='encode'):
    newres=[]
    for ares in result:
        grp=[]
        for elem in ares:
            if method=='encode':
                grp.append(elem.encode('utf8'))
            else:
                grp.append(elem.decode('utf8'))
        newres.append(grp)
    return newres



def parse_first_journal(query):
    """
    Uses pyparsing with grammar

    this splits into a list of ['+','word','literal'] 

    """

    yy=atpic.log.setname(xx,'parse')
    atpic.log.debug(yy,'input',query)
    query=query.decode('utf8')
    # print(query)

    sign=oneOf('+ -')
    modifier=Combine(oneOf("uid aid method") + Literal(":").suppress() ) # geopath
    # aword=Regex(r"[^ ]+", re.UNICODE) # non-space chars
    aword=Regex("[^ ]+") # non-space chars
    literal=dblQuotedString | aword
    term=Group(Optional(sign,"+")+Optional(modifier,"word")+literal) # default "+word"
    expr=OneOrMore(term)

    # now we can continue simplfying (normalize)
    # literal.setParseAction(removeQuotes)
    dblQuotedString.setParseAction(removeQuotes)

    result=expr.parseString(query)
    # print(result)

    newres=myencode(result)
    atpic.log.debug(yy,'output=',newres)
    return newres




# ====================================================
# 
#  2nd parsing
#
# =====================================================
# detect ranges

# used for dates ranges and number ranges
# http://rephrase.net/days/07/04/pyparsing
# http://crpppc19.epfl.ch/doc/python-pyparsing/htmldoc/frames.html

# date parsing from:
# http://pyparsing.wikispaces.com/message/view/home/58349466#58354510

 

def parse_wordorrange_pyparse(query):
    # returns pyparse object
    # 2012
    # 2012to2013
    # 2012,1013
    # ]2012,1013]
    # [2012,1013]
    # [2012to2013]

    yy=atpic.log.setname(xx,"parse_wordorrange_pyparse")
    query=query.decode('utf8')
    TO=oneOf('to ,',caseless=True).suppress()
    bracket=oneOf('[ ]')
    aword=Regex("[0-9\-\+\_:\.Zz\/]*") # non-space chars
    arange=Group(Optional(bracket,"[")('frombracket')+aword('fromword')+TO+aword('toword')+Optional(bracket,"]")('tobracket'))
    expression=arange('range')|aword('word')
    result=expression.parseString(query)
    print(result.asXML())

    print(result.dump())
    print('result.keys()=',result.keys())
    return result

def parse_wordorrange_py(result):
    # returns py nomral object
    yy=atpic.log.setname(xx,"parse_wordorrange_py")
    akeys=list(result.keys())
    print('akeys',akeys)
    if akeys==['range']:
        # returns a list of length 4
        out=[
            result.range.frombracket.encode('utf8'),
            result.range.fromword.encode('utf8'),
            result.range.toword.encode('utf8'),
            result.range.tobracket.encode('utf8'),
            ]
    else:
        # returns a list of length 1
        out=[result.word.encode('utf8')]

    print(out)
    return out

# expose this one
def parse_wordorrange(query):
    # returns 
    # a list of length 4 (a range)
    # or a list of length 1 (a number or word)
    return parse_wordorrange_py(parse_wordorrange_pyparse(query))


# =========================================
#
#   3rd parsing
#
# =========================================

# ========================================
#  number or fraction
# ========================================

def fraction2float(fraction):
    yy=atpic.log.setname(xx,"fraction2float")
    num=fraction['numerator']
    denu=fraction['denominator']
    num=float(num)
    denu=float(denu)
    res=num/denu
    return res

def parse_numberorfraction_pyparse(query):
    """
    Uses pyparsing with grammar
    """

    yy=atpic.log.setname(xx,'parse_numberorfraction_pyparse')
    atpic.log.debug(yy,'input',query)
    query=query.decode('utf8')
    atpic.log.debug(yy,query)
    divide = Literal('/')
    plusOrMinus = Literal('+') | Literal('-')
    decimalPoint = Literal('.')
    # to=oneOf('to TO tO To')
    integer = Combine(Optional(plusOrMinus) + Word(nums))
    number = (Combine(integer + Optional(decimalPoint + Word(nums))))('number')
    fraction = Group(number('numerator') + divide.suppress() + number('denominator'))('fraction')

    expression=fraction('fraction') | number('number')

    result=expression.parseString(query)
    print(result.asXML())
    print(result.dump())
    print(result.keys())
    return result


def parse_numberorfraction_py(result):
    # a range of number to json
    yy=atpic.log.setname(xx,"parse_numberorfraction_py")
    akeys=list(result.keys())
    print('akeys',akeys)
    if akeys==['fraction']:
        out=fraction2float(result['fraction'])
    else: # number
        # returns a list of length 1
        out=result['number']
    out=atpic.mybytes.float2bytes(out)
    print(out)
    atpic.log.debug(yy,'will return',out)
    return out

# expose this one
def parse_numberorfraction(query):
    return parse_numberorfraction_py(parse_numberorfraction_pyparse(query))

# longitude, latitude bbox
# (latitude 4.60°N, longitude 101.07°E)
# 4°60'N 101°7'E
# That's 4 degrees, 60 minutes
# ° - degrees
# ' - minutes
# " - seconds
# coord:4.5N_101E,10N99E
# coord:-101,45,-80,50

if __name__ == "__main__":
    query='+Type:video -type:mp4 paris'
    print(parse_first(query.encode('utf8')))
    # parse_bbox_pyparse(b'-10,+45TO10,+50.65')
    a=parse_wordorrange_pyparse(b'2011to2012')
    print(a)


    query='+aid:2 -uid:2 +method:post'
    print(parse_first_journal(query.encode('utf8')))
