#!/usr/bin/python3
from pyparsing import *

divide = Literal('/')
plusOrMinus = Literal('+') | Literal('-')
decimalPoint = Literal('.')
to=oneOf('to TO - tO To')
integer = Combine(Optional(plusOrMinus) + Word(nums))
number = (Combine(integer + Optional(decimalPoint + Word(nums))))('number')
fraction = Group(number('numerator') + divide.suppress() + number('denominator'))('fraction')
fracornb=fraction('fraction') ^ number('number')
rangeto=Group(fracornb('from') + to.suppress() + fracornb('to'))('range')

expression=(rangeto ^ fracornb)

res=expression.parseString("10/34TO100.0")
res=expression.parseString("10/34")
res=expression.parseString("1000")
# a=ParseResults(res)
print(res.asXML())
print(res.dump())
print(res.keys())
# print(res['range']['from'].dump())
