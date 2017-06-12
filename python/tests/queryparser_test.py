#!/usr/bin/python3
# -*- coding: utf-8 -*-
import atpic.queryparser
import unittest

class queryparser_test(unittest.TestCase):
    """USER legacy urls"""

    def test_parse_first(self):

        tests=[
            ("alex madon",[['+', 'word', 'alex'], ['+', 'word', 'madon']]),
            ("+alex -madon",[['+', 'word', 'alex'], ['-', 'word', 'madon']]),
            ('+"alex madon" paris',[['+', 'word', 'alex madon'], ['+', 'word', 'paris']]),
            ("+uid:1 france",[['+', 'uid', '1'], ['+', 'word', 'france']]),
            ("+Type:video -type:mp4 paris",[['+', 'Type', 'video'], ['-', 'type', 'mp4'], ['+', 'word', 'paris']]),
            ('+"Clara cet été là"',[['+', 'word', 'Clara cet été là']]),
            ("cet +été",[['+', 'word', 'cet'], ['+', 'word', 'été']]),
            ("+hello!",[['+', 'word', 'hello!']]),
            ('"hello Alex!"',[['+', 'word', 'hello Alex!']]),
            ('"hello, Alex!"',[['+', 'word', 'hello, Alex!']]),
            ("NONEXIST:alex",[['+', 'word', 'NONEXIST:alex']]),
            ("NONEXIST: alex",[['+', 'word', 'NONEXIST:'], ['+', 'word', 'alex']]),
            ("f:5.6",[['+', 'f', '5.6']]),
            ("f:5.6TO8",[['+', 'f', '5.6TO8']]),
            ("f:5.6to8",[['+', 'f', '5.6to8']]),
            ("f:5.6-8",[['+', 'f', '5.6-8']]),
            ("speed:1/500",[['+', 'speed', '1/500']]),
            ("speed:1/500to1/60",[['+', 'speed', '1/500to1/60']]),
            ("speed:1/500-1/60",[['+', 'speed', '1/500-1/60']]),
            ("speed:0.5-10",[['+', 'speed', '0.5-10']]),
            ("price:0-12.0",[['+', 'price', '0-12.0']]),
            ('私の名前は中野です',[['+', 'word','私の名前は中野です']]),
            ("lat:10to20.5",[['+', 'lat', '10to20.5']]),
            ("lon:-10to-5.0",[['+', 'lon', '-10to-5.0']]),
            ("date:2012",[['+', 'date', '2012']]),
            ("date:2012-12-31@23:40 alex madon",[['+', 'date', '2012-12-31@23:40'] ,['+', 'word', 'alex'],['+', 'word', 'madon']]),
            ]
        
        i=0
        for (query,expected) in tests:
            print("-------------------",i)
            print("%s" % query)
            res=atpic.queryparser.parse_first(query.encode('utf8'))
            print('ZZZ',res)
            print('XXX (\'',query,'\',',atpic.queryparser.mydecode(res),'),',sep='')

            self.assertEqual(atpic.queryparser.mydecode(res),expected)



    def test_parse_2nd(self):
        inputs=(
            (b'2010', [b'2010']) ,
            (b'2010-12', [b'2010-12']) ,
            (b'2010-12-31', [b'2010-12-31']) ,
            (b'2010to2011', [b'[', b'2010', b'2011', b']']) ,
            (b'2010-12TO2011', [b'[', b'2010-12', b'2011', b']']) ,
            (b'2010-12-31TO2011', [b'[', b'2010-12-31', b'2011', b']']) ,
            (b'2010-12-31TO2011-12', [b'[', b'2010-12-31', b'2011-12', b']']) ,
            (b'2010-12-31TO2011-12-31', [b'[', b'2010-12-31', b'2011-12-31', b']']) ,
            (b'2010,2011', [b'[', b'2010', b'2011', b']']) ,
            (b'[2010-12,2011]', [b'[', b'2010-12', b'2011', b']']) ,
            (b'[2010/12/31,2011]', [b'[', b'2010/12/31', b'2011', b']']) ,
            (b'[2010/12/31,', [b'[', b'2010/12/31', b'', b']']) ,
            (b',2011]', [b'[', b'', b'2011', b']']) ,
            (b',2011', [b'[', b'', b'2011', b']']) ,
            (b'2011,', [b'[', b'2011', b'', b']']) ,
            (b'-10.0to+20', [b'[', b'-10.0', b'+20', b']']) ,
            (b'1/500to1/60', [b'[', b'1/500', b'1/60', b']']) ,
            (b'1/500,1/60', [b'[', b'1/500', b'1/60', b']']) ,
            (b',1/60', [b'[', b'', b'1/60', b']']) ,
            (b'5.6to8.0', [b'[', b'5.6', b'8.0', b']']) ,
            (b'5.6,8.0', [b'[', b'5.6', b'8.0', b']']) ,
           )
        i=0
        for (query,expected) in inputs:
            i=i+1
            print('++++++++++++++++++',i,'+++++++++++++++++')
            print(query,'=>')
            res=atpic.queryparser.parse_wordorrange(query)
            print('YYY',(query,res),',')
            self.assertEqual(res,expected)


    def test_parse3rd(self):
        inputs=(
            (b'1/500', b'0.002') ,
            (b'1.5', b'1.5') ,
            (b'5.6', b'5.6') ,
            (b'8.0', b'8.0') ,
            (b'1/60', b'0.016666666666666666') ,
            )
        i=0
        for (query,ex) in inputs:
            i=i+1
            print('++++++++++++++++++',i,'+++++++++++++++++')
            res=atpic.queryparser.parse_numberorfraction(query)
            print('ZZZ',(query,res),',')
            self.assertEqual(res,ex)

 


if __name__=="__main__":
    unittest.main()
