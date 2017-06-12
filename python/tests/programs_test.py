# import atpic.authenticate


import unittest

class programs_test(unittest.TestCase):
    """USER legacy urls"""


    def testThumbnailer(self):
        """Legacy User ID"""
        import os
        file="/usr/bin/totem-gstreamer-video-thumbnailer"
        test=os.access(file, os.X_OK)
        self.assertEqual(test,True)

