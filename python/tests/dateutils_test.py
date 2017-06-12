#!/usr/bin/python3
import unittest
import atpic.dateutils


class worker_test(unittest.TestCase):
    """USER legacy urls"""

    def NOtest_dates(self):
        inputs=[
            (b'2011-06-18 13:47:02',b'2011-06-18T13:47:02.000000Z'),
            (b'2011-06-18 13:47:02.006',b'2011-06-18T13:47:02.006000Z'),
            (b'2011-06-18 13:47:02.000006',b'2011-06-18T13:47:02.000006Z'),
            ]
        for (sql,isoex) in inputs:
            iso=atpic.dateutils.date_sql2iso(sql)
            print(sql,'=>',iso)
            # self.assertEqual(iso,isoex)

    def NOtest_dateselas(self):
        inputs=[
            (b'2011-06-18 13:47:02', b'20110618134702000000'),
            (b'2011-06-18 13:47:02.006', b'20110618134702006000'),
            (b'2011-06-18 13:47:02.000006', b'20110618134702000006'),
            ]
        for (sql,isoex) in inputs:
            iso=atpic.dateutils.date_sql2elastic(sql)
            print('XXX',(sql,iso),',')
            self.assertEqual(iso,isoex)





    def NOtest_dateone(self):
        inputs=(  
            (b'2010', b'year', b'2010'),
            (b'201012', b'yearmonth', b'201012'),
            (b'20101231', b'yearmonthday', b'20101231'),
            (b'2010-12', b'yearmonth', b'201012'),
            (b'2010-12-31', b'yearmonthday', b'20101231'),
            (b'2010/12', b'yearmonth', b'201012'),
            (b'2010/12/31', b'yearmonthday', b'20101231'),
            (b'2011-06-18 13:47', b'yearmonthdaytime', b'20110618134700000000'),
            (b'2011-06-18 13:47:02', b'yearmonthdaytime', b'20110618134702000000'),
            (b'2011-06-18 13:47:02.006', b'yearmonthdaytime', b'20110618134702006000'),
            (b'2011-06-18 13:47:02.000006', b'yearmonthdaytime', b'20110618134702000006'),
           )
        i=0
        for (date,typex,datex) in inputs:
            i=i+1
            print('++++++++++++++++',i,'++++++++++++++++++')
            print(date)
            (mytype,dater)=atpic.dateutils.get_datefieldvalue(date)
            print('XXX', (date,mytype,dater),',')
            self.assertEqual((mytype,dater),(typex,datex))

    def NOtest_datetwo(self):
        inputs=( 
            (b'2010', b'2011', b'[', b']', b'year', b'2010', b'2011'),
            (b'2010', b'2011-12', b'[', b']', b'yearmonth', b'201000', b'201112'),
            (b'2010', b'2011-12-31', b'[', b']', b'yearmonthday', b'20100000', b'20111231'),
            (b'2010', b'2011-12-31 14:59', b'[', b']', b'yearmonthdaytime', b'20100000000000000000', b'20111231145999999999'),
            (b'2010/12/31', b'2011-12', b'[', b']', b'yearmonthday', b'20101231', b'20111299'),
            )
        i=0
        for (datefrom,dateto,bracket_from,bracket_to,typex,fromex,toex) in inputs:
            i=i+1
            print('++++++++++++++++',i,'++++++++++++++++++')
            print((datefrom,dateto,))
            (mytype,datefromr,datetor)=atpic.dateutils.get_datefieldrangevalue(datefrom,dateto,bracket_from,bracket_to)
            print('YYY',(datefrom,dateto,bracket_from,bracket_to,mytype,datefromr,datetor),',')
            self.assertEqual((mytype,datefromr,datetor),(typex,fromex,toex))


    def test_datetuple(self):
        inputs=(
            (b'2012-11-26T20:38:46.102717',),
            )
        i=0
        for (date,) in inputs:
            i=i+1
            print('++++++++++++++++',i,'++++++++++++++++++')
            (year,month,day,hour,minute)=atpic.dateutils.date_sql2tuple(date)
            print((date,year,month,day,hour,minute))
if __name__=="__main__":
    unittest.main()
