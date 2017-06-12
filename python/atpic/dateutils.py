#!/usr/bin/python3

import datetime
import re
import time


import atpic.log

xx=atpic.log.setmod("INFO","worker")

def date_sql2iso(datefirst): # strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    """
    Converts SQL time to XML time
    converts sql date to xml or json time
    """
    # there is no RFC for XML datetime?
    # rather based on ISO 8601
    # It is expressed in the format [-][Y*]YYYY-MM-DDThh:mm:ss[.s[s*]][TZD].
    # 2002-03-21T19:47:35Z
    yy=atpic.log.setname(xx,'get_datexml')

    parsed=False
    try:
        # try to parse with microseconds
        datetimefirst=datetime.datetime.strptime(datefirst.decode('utf8'),"%Y-%m-%d %H:%M:%S.%f" )
        parsed=True
    except:
        pass
    if not parsed:
        # parse with seconds
        datetimefirst=datetime.datetime.strptime(datefirst.decode('utf8'),"%Y-%m-%d %H:%M:%S" )

    datexml=datetimefirst.strftime("%Y-%m-%dT%H:%M:%S.%fZ").encode('utf8')


    return datexml

def elastic_now():
    yy=atpic.log.setname(xx,'elastic_now')
    timenow=time.time()
    atpic.log.debug(yy,'timenow',timenow)
    datetimefirst=datetime.datetime.fromtimestamp(timenow)
    datejson=datetimefirst.strftime("%Y-%m-%dT%H:%M:%S.%fZ").encode('utf8')
    return datejson

def date_sql2tuple(date):
    year=date[0:4]
    month=date[5:7]
    day=date[8:10]
    hour=date[11:13]
    minute=date[14:16]
    return (year,month,day,hour,minute)

def date_sqlyear(date): # strftime("%Y")
    return date[0:4]

def date_sqlyearmonth(date): # strftime("%Y%m")
    return date[0:4]+date[5:7]

def date_sqlyearmonthday(date): # strftime("%Y%m%d")
    return date[0:4]+date[5:7]+date[8:10]

def date_sql2elastic(date):
    # remove all non digits chars
    # note this asume that months are written with 2 digists and days too
    datedigts=re.sub(b'[^0-9]',b'',date)
    # padding
    dateelas=datedigts.ljust(20,b'0')
    return dateelas




# used in elasticsearch where you have various resolutions for date

def remove_nondigits(date):
    datedigts=re.sub(b'[^0-9]',b'',date)
    return datedigts

def get_datefieldrangevalue(datefrom,dateto,bracket_from,bracket_to):
    # select the filed 'year', 'yearmonth', etc..
    # based on the two values (datefrom,dateto)
    # date input can be any valid '2012' '2012/12/31' etc..
    mytype=b'year'
    datefrom=remove_nondigits(datefrom)
    dateto=remove_nondigits(dateto)
    if bracket_from==b'[':
        padding_from=b'0'
    else:
        padding_from=b'9'

    if bracket_to==b']':
        padding_to=b'9'
    else:
        padding_to=b'0'

    lend=max(len(datefrom),len(dateto))

    if lend==4:
        mytype=b'year'
        datefrom=datefrom.ljust(4,padding_from)
        dateto=dateto.ljust(4,padding_to)
    elif lend==6:
        mytype=b'yearmonth'
        datefrom=datefrom.ljust(6,padding_from)
        dateto=dateto.ljust(6,padding_to)
    elif lend==8:
        mytype=b'yearmonthday'
        datefrom=datefrom.ljust(8,padding_from)
        dateto=dateto.ljust(8,padding_to)
    elif lend>8:
        mytype=b'yearmonthdaytime'
        datefrom=datefrom.ljust(20,padding_from)
        dateto=dateto.ljust(20,padding_to)

    return (mytype,datefrom,dateto)

def get_datefieldvalue(date):
    # date input can be any valid '2012' '2012/12/31' etc..
    # returns a (datefield, datevalue)
    mytype=b''
    date=remove_nondigits(date)
    lend=len(date)
    if lend==4:
        mytype=b'year'
    elif lend==6:
        mytype=b'yearmonth'
    elif lend==8:
        mytype=b'yearmonthday'
    elif lend>8:
        mytype=b'yearmonthdaytime'
        date=date.ljust(20,b'0')
    return (mytype,date)

def date_exif2sql(adate):
    """
    select _exifdatetimeoriginal,_datetimeoriginalsql from _user_gallery_pic limit 3;
 _exifdatetimeoriginal | _datetimeoriginalsql 
-----------------------+----------------------
 2012:06:02 13:55:26   | 2012-06-02 13:55:26
 2010:09:18 20:03:47   | 2010-09-18 20:03:47
 2011:12:25 23:02:58   | 2011-12-25 23:02:58
 """
    # try to parse with microseconds
    try:
        bdate=datetime.datetime.strptime(adate.decode('utf8'),"%Y:%m:%d %H:%M:%S" )
        sqldate=bdate.strftime("%Y-%m-%d %H:%M:%S.%f").encode('utf8')
    except:
        sqldate=b''
    return sqldate


if __name__ == "__main__":
    print(date_sql2iso(b'2011-06-18 13:47:02'))
    print(date_sqlyear(b'2011-06-18 13:47:02'))
    print(date_sqlyearmonth(b'2011-06-18 13:47:02'))
    print(date_sqlyearmonthday(b'2011-06-18 13:47:02'))
    print(date_exif2sql(b'2011:12:25 23:02:58'))
