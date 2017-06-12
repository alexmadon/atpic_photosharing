#!/usr/bin/python3
from pyparsing import *

divide = Literal('/')
plusOrMinus = Literal('+') | Literal('-')
decimalPoint = Literal('.')
integer = Combine(Optional(plusOrMinus) + Word(nums))
number = (Combine(integer + Optional(decimalPoint + Word(nums))))('number')
# fraction = Group(number('numerator') + divide.suppress() + number('denominator')).setResultsName('fraction', listAllMatches=True)
fraction = Group(number('numerator') + divide.suppress() + number('denominator'))('fraction')
expression=OneOrMore(fraction)('expression')

string="1/500"
parseTree = fraction.parseString(string)
print(parseTree)
print(parseTree.keys())
print(number.parseString("435.89999"))
res=expression.parseString("5/999 2/333 10/100")
a=ParseResults(res)
print(a.asXML())
print(a.items())
print(a.keys())
print(a['fraction'])
print('+++++++++++++++++++')
for b in a['expression']:
    print("id(b)",id(b))
    print('b.__name__()',type(b))
    print('b.items()',b.items())
    print('b.keys()',b.keys())
    print('b',b)
    print('b.dump()',b.dump())
print('+++++++++++++++++++')
print(a.dump())

print('ccc',a.items())
namedItems = dict( [ (v[1],k) for (k,vlist) in a.items()
                     for v in vlist ] )
print(namedItems)
"""
valuemap = dict((id(v),k) for k,v in a.list.items())
for t in tokens.list:
    if id(t) in valuemap:
        print (valuemap[id(t)])
    else:
        print ("<none>")
    print (t)
"""
