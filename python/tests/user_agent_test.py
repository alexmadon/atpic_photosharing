#!/usr/bin/python3
import unittest


import atpic.user_agent


# http://msdn.microsoft.com/en-us/library/bb159684.aspx
# http://www.botsvsbrowsers.com/


# Originally, the HTTP User Agent headers used by Internet Explorer Mobile are different and depended on the platform. They included both the kind of device and the size of the screen in pixels For example Pocket PC for Windows Mobile Version 5.0 and before devices will use the header: 


mobiles=[]
mobiles.append("Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; PPC; 240x320)")

# The original User Agent header for Smartphone for Windows Mobile Version 5.0 and before was:
mobiles.append("Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; Smartphone; 176x220)")

# With Windows Mobile 6 the HTTP User Agent header includes identification of the browser. For example the User Agent header for Windows Mobile 6 is as follows:

mobiles.append("Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile M.N)")


# http://forum.xda-developers.com/showthread.php?p=2190969

# Internet Explorer Mobile (IEM)

# WM6.0 Classic (HP iPAQ 210, official ROM):
mobiles.append("Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 7.7)")

# WM6.0 Standard (HTC S710 with the January official ROM upgrade):
mobiles.append("Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 7.6) SP; 240")
mobiles.append("x320; HTC_S710/1.0 Profile/MIDP-2.0 Configuration/CLDC-1.1")


# WM6.1 Pro (Cooked HTC Universal ROM):
mobiles.append("Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 7.11)")


# WM5:
mobiles.append("Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; PPC; 240x320)")

# Opera Mini 4.1 under Jbed 3.1:
mobiles.append("Opera/9.50 (J2ME/MIDP; Opera Mini/4.1.10781/302; U; en)")

# Opera Mobile 9.33b:
mobiles.append("Opera/9.0 (Microsoft Windows; PPC; Opera Mobile/331; U; en)")

# Opera Mobile 8.50:
mobiles.append("Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; PPC; 480x640) Opera 8.50 [en]")

# Current NetFront 3.5 TP
mobiles.append("Mozilla/5.0 (PDA; NF35WMPRO/1.0; like Gecko) NetFront/3.5")



# NetFront 3.3 final
mobiles.append("Mozilla/4.08 (PDA; NF33PPC3AR/1.0) NetFront/3.3")

# Thunderhawk
mobiles.append("Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:0.9.5) Gecko/20011018")

# Other mobile OSes

# Symbian S60 FP1: Nokia S60 Web (on the N95 v21):
mobiles.append("Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95/21.0.016; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413")


# iPhone Safari:

mobiles.append("Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3B48b Safari/419.")





# On desktop Windows:
mobiles.append("Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 2.0.50727; FDM; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30)")

# IE8:
mobiles.append("Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 2.0.50727; FDM; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30)")
# Connection: Keep-Alive

# Opera 9.5b:
mobiles.append("Opera/9.50 (Windows NT 5.1; U; en)")

# Mozilla/Firefox 3b5:
mobiles.append("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13")






notmobiles=[]
notmobiles.append("Mozilla/4.0")



class dispatcherURLtest(unittest.TestCase):
    """USER legacy urls"""


    def testMobiles(self):
        """Testing Dispatcher"""
        environ={}
        for agent in mobiles:
            environ["HTTP_USER_AGENT"]=agent
            print("testing %s" % agent)
            self.assertEqual(atpic.user_agent.parse_header(environ),True)

    def testNotMobiles(self):
        """Testing Dispatcher"""
        environ={}
        for agent in notmobiles:
            environ["HTTP_USER_AGENT"]=agent
            print("testing %s" % agent)
            self.assertEqual(atpic.user_agent.parse_header(environ),False)



if __name__=="__main__":
    unittest.main()
