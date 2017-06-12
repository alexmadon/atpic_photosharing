import unittest
import atpic.xss_protect


check_test = (

('# basics',),
("",""),
("hello","hello"),
("""<a href="http://google.com">http://google.com</a><img src="http://google.com/img.gif"/>""","""<a href="http://google.com">http://google.com</a><img src="http://google.com/img.gif"/>"""),
)

class xss_filter_test(unittest.TestCase):
    """html filter"""

    
    def test_go(self):
        """tests the filter.strip() function"""
        filter = atpic.xss_protect.XssCleaner()
        for test in check_test:
            if len(test) == 1:
                # we set an option for the filter
                # print "**************************"
                # print test[0]
                exec(test[0])
            else:
                # we check the option
                ret = filter.strip(test[0])
                print("%s => %s" % (test[0],ret))
                self.assertEqual(ret,test[1])
                # also sanity check: calling twice the function
                ret2 = filter.strip(ret)
                self.assertEqual(ret2,ret)



if __name__ == "__main__":
    unittest.main()
