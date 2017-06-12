#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest



import atpic.xmlutils



# logger=mysetlogger(quiet=False)

class xmlutils_test(unittest.TestCase):
    """USER legacy urls"""

    def NOtest_good(self):




        xml_strings_good=(
            b"""<USER url="http://atpic.faa/user/1"><rows>0</rows><synced>None</synced><css>1</css><lang>fr</lang><login>alexmadon</login><fastdir_atpic>/hdc1/fastdir/atpic</fastdir_atpic><template>0</template><id>11</id><fastdir_atpic_ln>/hdc1/fastdir_ln/atpic</fastdir_atpic_ln><fasturl_atpic>http://46.4.24.136/atpic</fasturl_atpic><datelast>None</datelast><thestyleid>1</thestyleid><size_allowed>None</size_allowed><storeto>None</storeto><servername>user6.atpic.com</servername><email>alex@example.foo</email><servershort>alex</servershort><serverip>46.4.24.136</serverip><mount>/hdc1</mount><cols>0</cols><text>a &amp;b</text><device>/dev/sda3</device><password>salted</password><title></title><counter>15396</counter><storefrom>12</storefrom><datefirst>None</datefirst><name>Alex M</name><GALLERY url="http://alex.atpic.faa/gallery/1"><rows>0</rows><file></file><skin_pic>0</skin_pic><priority></priority><css_gallery>2</css_gallery><css_pic>2</css_pic><id>22</id><mode>b</mode><datelast>2008-09-02 15:24:22.036494</datelast><template_pic>0</template_pic><bgcolor></bgcolor><style>2</style><cols>4</cols><secret>0</secret><text>Some macro photos I took with my powershot.</text><title>Macro</title><lon>None</lon><fgcolor></fgcolor><counter>4744</counter><lat>None</lat><datefirst>2004-02-11 00:00:00</datefirst><template_gallery>0</template_gallery><dir>3</dir><isroot>n</isroot><skin_gallery>0</skin_gallery><user>1</user><pic url="http://alex.atpic.faa/gallery/1/pic/2090536"><width>None</width><make>None</make><r350>2012-01-10 20:51:50.109940</r350><priority>None</priority><datetimedigitized>None</datetimedigitized><link>None</link><id>33333</id><focallength>None</focallength><notpop>0</notpop><flash>None</flash><aperture>None</aperture><exposuretime>None</exposuretime><sensingmethod>None</sensingmethod><datelast>None</datelast><gallery>1</gallery><sizeb>None</sizeb><extension>None</extension><bgcolor>None</bgcolor><done>None</done><r1024>2012-01-10 20:51:50.109940</r1024><height>None</height><datetimeoriginal>None</datetimeoriginal><meteringmode>None</meteringmode><originalname>None</originalname><text>None</text><reviewed>0</reviewed><r70>2012-01-10 20:51:50.109940</r70><title>None</title><lon>None</lon><fgcolor>None</fgcolor><model>None</model><counter>0</counter><exposuremode>None</exposuremode><lat>None</lat><whitebalance>None</whitebalance><datefirst>2012-01-10 20:51:50.109940</datefirst><datetimeoriginalsql>None</datetimeoriginalsql><r160>2012-01-10 20:51:50.109940</r160><revaccepted>0</revaccepted><r600>2012-01-10 20:51:50.109940</r600><user>1</user><isospeedratings>None</isospeedratings></pic></GALLERY></USER>""",
            )
        for xml_string in xml_strings_good:
            path=atpic.xmlutils.get(xml_string,b'/USER/fastdir_atpic')
            print(path)
            path_expected=b"/hdc1/fastdir/atpic"
            self.assertEqual(path,path_expected)
            # self.assertEqual(res,result)

            
            results=atpic.xmlutils.get_new_image_params(xml_string)
            print(results)
            results_expected=(b'/hdc1', b'11', b'22', b'33333', b'2012-01-10 20:51:50.109940')
            self.assertEqual(results,results_expected)

            

    def NOtest_bad(self):



        xml_strings_bad=(
            """<notok><error><code>404</code><message>pattern post uname_gallery_ is not valid</message></error><post><post></post></post></notok>""",
            """<notok><error><code>401</code><message>Data error</message></error><authenticated><uid>1</uid><short>alex</short><displayname>Alex M</displayname></authenticated><post><post></post></post></notok>""",
            )
        for xml_string in xml_strings_bad:
            self.assertRaises(atpic.xmlutils.XMLnotValid,atpic.xmlutils.get_new_image_params,xml_string) # exception



    def test_replace(self):
        inputs=(
            (
                b'<a><b><b1>alex</b1><b2>madon</b2><d></d></b><c>Hi</c></a>',
                b'/a/b',
                {b'b1':b'ALEX',b'b2':b'DOE',b'd':b'MADON'},
                b'<a><b><b1>ALEX</b1><b2>DOE</b2><d>MADON</d></b><c>Hi</c></a>'
                ),
            (
                b'<a><b><b1>alex</b1><d></d></b><c>Hi</c></a>',
                b'/a/b',
                {b'b1':b'ALEX',b'b2':b'DOE',b'd':b'MADON'},
                b'<a><b><b1>ALEX</b1><d>MADON</d><b2>DOE</b2></b><c>Hi</c></a>'
                ),
            )
           


        for (xml_string,basepath,anarray,expected) in inputs:
            ss=atpic.xmlutils.replace_params(xml_string,basepath,anarray)
            self.assertEqual(ss,expected)


if __name__=="__main__":
    unittest.main()
