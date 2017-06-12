import atpic.syslogparser
import unittest
import os


class syslog_test(unittest.TestCase):
    """html filter"""

    
    def test_sample(self):
        """filer syslog call 1"""
        import StringIO
        file=open('fixture/samplelog1.txt', 'r')
        expectedoutput="""p\t1009173\t1
p\t1009178\t1
"""

        outfile= StringIO.StringIO("")
        outfile=atpic.syslogparser.parse_iostring(file,outfile)
        output=outfile.getvalue()
        # print output
        self.assertEqual(output,expectedoutput)

    def test_sample2(self):
        """Using a pipe
        
        Equivalent of:
        
        cat fixture/samplelog1.txt | python ../atpic/syslogparser.py
        
        """
        import subprocess
        p1 = subprocess.Popen(
            ["cat","fixture/samplelog1.txt"], 
            stdout=subprocess.PIPE)
        p2 = subprocess.Popen(
            ["python", "../atpic/syslogparser.py"], stdin=p1.stdout, 
            stdout=subprocess.PIPE)
        output = p2.communicate()[0]
        expectedoutput="""p\t1009173\t1
p\t1009178\t1
"""
        # print output
        self.assertEqual(output,expectedoutput)


if __name__ == "__main__":
    unittest.main()
