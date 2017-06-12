import unittest
import os
import sys
import atpic.installerat

class installer_test(unittest.TestCase):
    """Test the installer test functions"""
    def testFind(self):
        file="fixture/matcher.txt"
        nb=atpic.installerat.check_file_match_re("GOOD",file)
        print nb

class install_test(unittest.TestCase):
    """USER legacy urls"""


    def testSyslogExist(self):
        """We need syslog-ng"""
        path="/etc/syslog-ng/syslog-ng.conf"
        exist=os.path.exists(path)
        # print "Exist: %s" % exist
        self.assertEqual(
            True,
            exist,
            "%s is missing: it seems you don't have syslog-ng installed."%path)

    def testSyslogDate(self):
        """ checks if the syslog-ng.conf file contains:
        ts_format(iso)
        which is needed for page view count
        """


#    def testftp(self):
#        from ftplib import FTP
#        ftp = FTP("u1.up.atpic.com","someuser","somepass")
#        ftp.dir()
#        ftp.quit()
    

if __name__ == "__main__":
    unittest.main()
