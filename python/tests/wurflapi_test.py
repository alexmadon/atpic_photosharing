#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import urllib.parse
import io



import atpic.worker
import atpic.wurflapi




user_agents=(
    (b'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1 Iceweasel/7.0.1',b'd|xhtml'),
    (b'Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; PPC; 240x320)',b'm|xhtml|240|320|228|310'),
    (b'Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; Smartphone; 176x220)',b'm|xhtml|320|240|310|220'),
    (b'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile M.N)',b'm|xhtml|240|320|228|280'),
    (b'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 7.7)',b'm|xhtml|240|320|228|280'),
    (b'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 7.6) SP; 240',b'm|xhtml|320|240|300|200'),
    (b'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.12) SP; 240x320; HTC_S710/1.0 Profile/MIDP-2.0 Configuration/CLDC-1.1',b'm|xhtml|240|320|240|300'),
    (b'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 7.11)',b'm|xhtml|480|640|470|620'),
    (b'Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; PPC; 240x320)',b'm|xhtml|240|320|228|310'),
    (b'Opera/9.50 (J2ME/MIDP; Opera Mini/4.1.10781/302; U; en)',b'm|xhtml|176|160|165|140'),
    (b'Opera/9.0 (Microsoft Windows; PPC; Opera Mobile/331; U; en)',b'd|xhtml'),
    (b'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; PPC; 480x640) Opera 8.50 [en]',b'd|html'),
    (b'Mozilla/5.0 (PDA; NF35WMPRO/1.0; like Gecko) NetFront/3.5',b'm|xhtml|240|320|224|300'),
    (b'Mozilla/4.08 (PDA; NF33PPC3AR/1.0) NetFront/3.3',b'm|html|120|100|120|92'),
    (b'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:0.9.5) Gecko/20011018',b'd|xhtml'),
    (b'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95/21.0.016; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',b'm|xhtml|240|320|224|280'),
    (b'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3B48b Safari/419.',b'm|xhtml|320|480|320|360'),
    (b'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 2.0.50727; FDM; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30)',b'd|html'),
    (b'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 2.0.50727; FDM; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30)',b'd|html'),
    (b'Opera/9.50 (Windows NT 5.1; U; en)',b'd|xhtml'),
    (b'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13',b'd|xhtml'),
    (b'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',b'd|html'),
)

class wurlf_test(unittest.TestCase):
    """USER legacy urls"""

    def NOtest_agent(self):
        i=0
        for (agent,res) in user_agents:
            i=i+1
            print("+++++++++++++++++++++++++",i,"+++++++++++++++++++++++")
            print(agent)
            user_agent=atpic.wurflex.sxmlw(agent)
            # self.assertEqual(res,result)
            # xmlo=None
            # xmlo=atpic.xmlob.Xmlo()
            # rediscon=None
            serialized=atpic.wurflapi.set_wurfl_solr(user_agent)
            print(serialized)
            # print(b''.join(xmlo.datastack))
            print('XXXX (',agent,',',serialized,'),',sep="")
            self.assertEqual(res,serialized)





    def test_serial(self):
        tests=(
            (b'd|xhtml',{b'wformat': b'xhtml', b'type': b'desktop'}),
            (b'm|xhtml|240|320|228|310',{b'resolution_width': b'240', b'resolution_height': b'320', b'max_image_width': b'228', b'max_image_height': b'310', b'wformat': b'xhtml', b'type': b'mobile'}),
            (b'm|xhtml|320|240|310|220',{b'resolution_width': b'320', b'resolution_height': b'240', b'max_image_width': b'310', b'max_image_height': b'220', b'wformat': b'xhtml', b'type': b'mobile'}),
            (b'm|xhtml|240|320|228|280',{b'resolution_width': b'240', b'resolution_height': b'320', b'max_image_width': b'228', b'max_image_height': b'280', b'wformat': b'xhtml', b'type': b'mobile'}),
            (b'm|xhtml|240|320|228|280',{b'resolution_width': b'240', b'resolution_height': b'320', b'max_image_width': b'228', b'max_image_height': b'280', b'wformat': b'xhtml', b'type': b'mobile'}),
            (b'm|xhtml|320|240|300|200',{b'resolution_width': b'320', b'resolution_height': b'240', b'max_image_width': b'300', b'max_image_height': b'200', b'wformat': b'xhtml', b'type': b'mobile'}),
            (b'm|xhtml|240|320|240|300',{b'resolution_width': b'240', b'resolution_height': b'320', b'max_image_width': b'240', b'max_image_height': b'300', b'wformat': b'xhtml', b'type': b'mobile'}),
            (b'm|xhtml|480|640|470|620',{b'resolution_width': b'480', b'resolution_height': b'640', b'max_image_width': b'470', b'max_image_height': b'620', b'wformat': b'xhtml', b'type': b'mobile'}),
            (b'm|xhtml|240|320|228|310',{b'resolution_width': b'240', b'resolution_height': b'320', b'max_image_width': b'228', b'max_image_height': b'310', b'wformat': b'xhtml', b'type': b'mobile'}),
            (b'm|xhtml|176|160|165|140',{b'resolution_width': b'176', b'resolution_height': b'160', b'max_image_width': b'165', b'max_image_height': b'140', b'wformat': b'xhtml', b'type': b'mobile'}),
            (b'd|xhtml',{b'wformat': b'xhtml', b'type': b'desktop'}),
            (b'd|html',{b'wformat': b'html', b'type': b'desktop'}),
            (b'm|xhtml|240|320|224|300',{b'resolution_width': b'240', b'resolution_height': b'320', b'max_image_width': b'224', b'max_image_height': b'300', b'wformat': b'xhtml', b'type': b'mobile'}),
            (b'm|html|120|100|120|92',{b'resolution_width': b'120', b'resolution_height': b'100', b'max_image_width': b'120', b'max_image_height': b'92', b'wformat': b'html', b'type': b'mobile'}),
            (b'd|xhtml',{b'wformat': b'xhtml', b'type': b'desktop'}),
            (b'm|xhtml|240|320|224|280',{b'resolution_width': b'240', b'resolution_height': b'320', b'max_image_width': b'224', b'max_image_height': b'280', b'wformat': b'xhtml', b'type': b'mobile'}),
            (b'm|xhtml|320|480|320|360',{b'resolution_width': b'320', b'resolution_height': b'480', b'max_image_width': b'320', b'max_image_height': b'360', b'wformat': b'xhtml', b'type': b'mobile'}),
            (b'd|html',{b'wformat': b'html', b'type': b'desktop'}),
            (b'd|html',{b'wformat': b'html', b'type': b'desktop'}),
            (b'd|xhtml',{b'wformat': b'xhtml', b'type': b'desktop'}),
            (b'd|xhtml',{b'wformat': b'xhtml', b'type': b'desktop'}),
            (b'd|html',{b'wformat': b'html', b'type': b'desktop'}),
            )
        
        i=0
        for (serial,expect) in tests:
            i=i+1
            print("+++++++++++++++++++++++++",i,"+++++++++++++++++++++++")
            print(serial)
            res=atpic.wurflapi.parse_serial(serial)
            print('XXXX (',serial,',',res,'),',sep='')
            self.assertEqual(res,expect)

if __name__=="__main__":

    unittest.main()
