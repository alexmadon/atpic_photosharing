#!/usr/bin/python3



import atpic.authenticate
import atpic.libpqalex

import unittest






class authenticate_test(unittest.TestCase):
    """USER legacy urls"""


    
    def NOtestSession(self):
        """session creation"""
        userid=b'4344'
        timepart=b'337937'
        randompart=b'5njdcrvvcv'
        hashpart=atpic.authenticate.session_hashpart_make(userid,timepart,randompart)
        self.assertEqual(b'4344-337937-5njdcrvvcv-'+hashpart,b'4344-337937-5njdcrvvcv-7654e139730b9dc6f900')

    def NOtestValidSession(self):
        # validates the short sessions
        userid=b'1'
        session=atpic.authenticate.session_make(userid)
        userid_fromsession=atpic.authenticate.session_validate(session)
        print('userid_fromsession' ,userid_fromsession)
        self.assertEqual(userid,userid_fromsession)
        
    def NOtestInValidSession(self):
        sessions=[
            b"1-356608-kdzk71rtql-22fb1328ac58497652becb6dc7130048",
            b"2-356610-kdzk71rtql-22fb1328ac58497652becb6dc7130048",
            ]
        for session in sessions:
            # atpic.authenticate.session_validate(session)
            self.assertRaises(Exception,atpic.authenticate.session_validate,session)

    def NOtestSecret(self):
        secret=atpic.authenticate.secret_make()
        print("secret",secret)
        self.assertEqual(20,len(secret))
    def NOtest_base64username_decode(self):
        encoded=b'MXx0ZXN0bG9naW58TXIgVGVzdGVy'
        res=atpic.authenticate.base64username_decode(encoded)
        self.assertEqual((b'1',b'testlogin',b'Mr Tester'),res)

    def NOtestAuthenticate(self):
        environs=[
            ({b'HTTP_X_ATPIC_SESSION': b'1-356608-kdzk71rtql-22fb1328ac58497652becb6dc7130048'},(False, ())),
            ({b'HTTP_X_ATPIC_SESSION': b'2-356610-kdzk71rtql-22fb1328ac58497652becb6dc7130048'},(False, ())),
            ({b'HTTP_X_ATPIC_SESSION': atpic.authenticate.fullsession_make(b'1',b'testlogin', b'Mr Tester')},(True, (b'1', b'testlogin', b'Mr Tester'))),
            # ({'HTTP_COOKIE': 'session=1-367233-fyp8d-a92a760f303e28e3eb78-MXx0ZXN0bG9naW58TXIgVGVzdGVy-4860d2f710'},(True, (1, 'testlogin', 'Mr Tester'))),
            ({b'HTTP_AUTHORIZATION': b'Basic YWQ6YWQ='},(False, ())),
            ({b'HTTP_AUTHORIZATION': b'Basic YWxleG1hZG9uOnR1eDR0dXg='},(True, (b'1', b'alex', b'Alex M'))),
            ]
        i=0
        db=atpic.libpqalex.db()
        for (env,expected_res) in environs:
            i=i+1
            print('+++++++++ test %s +++++++++' % i)
            res=atpic.authenticate.authenticate(env,db)
            print('XXXX (',env,',',res,"),",sep='')
            self.assertEqual(res,expected_res)


if __name__=="__main__":
    print("ddd")
    unittest.main()

