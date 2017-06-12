# py3k version
import calendar
year=2008
calendar.prcal(year)



from time import time, ctime
the_time = ctime(time())
print(the_time)

print(time())



import calendar
import datetime
mytoday = datetime.datetime.today()
myyear = str(mytoday.year)
mymonth = str(mytoday.month)
calendar.setfirstweekday(calendar.SUNDAY)

print(calendar.month( 2003, 10 ))

calendar.prmonth( 2003, 10 )


# http://technofreakatchennai.wordpress.com/2007/11/24/pythonfinding-weeks-of-a-month/
import calendar
import time
y, m = time.localtime(time.time())[:2]
for i in calendar.month(y, m).split('\n')[2:-1]:
    print(i.split())

# output:
# ['1', '2', '3', '4', '5', '6']
# ['7', '8', '9', '10', '11', '12', '13']
# ['14', '15', '16', '17', '18', '19', '20']
# ['21', '22', '23', '24', '25', '26', '27']
# ['28', '29', '30', '31']



# http://article.gmane.org/gmane.comp.web.zope.plone.collective.cvs/67907
weekday, numDays = calendar.monthrange(2008, 12)
print(calendar.month(2008, 12))
calendar.setfirstweekday(calendar.SUNDAY)
print(calendar.monthrange(2008, 11))
calendar.setfirstweekday(calendar.MONDAY)
print(calendar.monthrange(2008, 11))



print(calendar.month(2008, 11))

# http://docs.python.org/lib/module-calendar.html
# http://svn.python.org/projects/python/trunk/Lib/calendar.py
