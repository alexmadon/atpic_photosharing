#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import filecmp
import io


import unittest
import urllib.parse

import atpic.getindata



class getindata_test(unittest.TestCase):
    """USER legacy urls"""

    def NOtest_save_multi(self):
        environs=[
            ({
                b'CONTENT_TYPE':b'content_type multipart/form-data; boundary=0123456789',
                b'wsgi.input':io.BytesIO(b"""--0123456789\r\nsomeheader1\r\n\r\nsomedata1\r\n--0123456789\r\nsomeheader2\r\n\r\nsomedata2\r\n--0123456789--\r\ncccccccccccc"""),
                },
             [(b'nocontentdisposition', True, (b'/tmp/atup67vh8y', b'', b'')), (b'nocontentdisposition', True, (b'/tmp/atup2993px', b'', b''))]),



            ({
                b'CONTENT_TYPE': b'multipart/form-data; boundary=---------------------------44318235148506958065901630',
                b'wsgi.input':open('fixture/corsica_multipart_firefox_utf8','rb'),
                },
             [(b'title', False, b'cet \xc3\xa9t\xc3\xa9 l\xc3\xa0'), (b'userfile', True, (b'/tmp/atupfh_dkq', b'corsica_from_space_small.jpg', b'image/jpeg'))]
             ),

            ({
                b'CONTENT_TYPE': b'multipart/form-data; boundary=---------------------------17286521591893302557554318847',
                b'wsgi.input':open('fixture/forms_multipart_utf8','rb'),
                },
             [(b'group1', False, b'Butter'), (b'food', False, b'\xc3\xa9t\xc3\xa9'), (b'food', False, b'automne'), (b'food', False, b'hiver'), (b'toppings', False, b'greenpeppers'), (b'toppings', False, b'onions'), (b'toppings', False, b'tomatoes')]
             ),
            


            ]


        i=0
        for (environ,alist_ex) in environs:
            i=i+1
            print("\n\n\n\n++++++++++++++++++++++++++++++++++",i,"+++++++++++++++++++++")
            alist=atpic.getindata.multipart_save(environ,b'/tmp')
            environ[b'wsgi.input'].close()
            print('XXX',alist,sep="")
            # self.assertEqual(dictsum,dictsum_expected)
            # self.assertEqual(len(flist),len(flist_expected))
            i=0
            for (aname,isfile,avalue) in alist:
                (aname_ex,isfile_ex,avalue_ex)=alist_ex[i]
                i=i+1
                if not isfile:
                    self.assertEqual(aname,aname_ex)
                    self.assertEqual(avalue,avalue_ex)
                else:
                    self.assertEqual(avalue[1:],avalue_ex[1:])


    # def NOtest_save_multi_error(self):
    #    environs=[
    #
    #        {
    #            'CONTENT_TYPE': 'multipart/related; boundary="END_OF_PART"',
    #            'wsgi.input':open('fixture/google_picassa_atom1','rb'),
    #            },
    #        ]
    #    for environ in environs:
    #        
    #        self.assertRaises(Exception,atpic.getindata.multipart_save,environ)


    def NOtest_parse_header(self):
        headers=(
            (b'Content-Disposition: form-data; name="userfile"; filename="corsica_from_space_small.jpg"',
             (b'CONTENT_DISPOSITION',
              b'form-data',
              {b'name': b'userfile', b'filename': b'corsica_from_space_small.jpg'},
              ),
             ),
            
            (b'Content-Disposition: form-data; name="title"',
             (b'CONTENT_DISPOSITION',
              b'form-data',
              {b'name': b'title'},
              ),
             ),

            (b'Content-Type: image/jpeg',
             (b'CONTENT_TYPE',
              b'image/jpeg',
              {},
              ),
             ),
            )

        for header in headers:
            parsed=atpic.getindata.parse_header(header[0])
            print(header[0])
            print("-->",parsed)
            self.assertEqual(parsed,header[1])



    # ------------
    # /tmp/atupxdh0qu
    # fixture/corsica_from_space_small.jpg
    # ------------
    # 'CONTENT_TYPE': 'multipart/form-data; boundary=----------------------------114a2d890e44'
    # fixture/corsica_multipart_curl  
    # ------------
    # 'CONTENT_TYPE': 'multipart/form-data; boundary=---------------------------163756941815518654241868925319'
    # fixture/corsica_multipart_firefox
    # ------------
    def NOtest_multipart_parse_disk(self):
        files=(
            ((b"fixture/corsica_multipart_curl",b"----------------------------114a2d890e44"),
             [
                    ({b'CONTENT_DISPOSITION': (b'form-data', {b'name': b'title'})}, 92, 98, b'fixture/file_title1'), 
                    ({b'CONTENT_DISPOSITION': (b'form-data', {b'name': b'upload', b'filename': b'corsica_from_space_small.jpg'}), b'CONTENT_TYPE': (b'image/jpeg', {})}, 260, 65459, b'fixture/corsica_from_space_small.jpg')]),

            ((b"fixture/corsica_multipart_firefox",b"---------------------------163756941815518654241868925319"),
             [
                    ({b'CONTENT_DISPOSITION': (b'form-data', {b'name': b'title'})}, 109, 125, b'fixture/file_clara'), 
                    ({b'CONTENT_DISPOSITION': (b'form-data', {b'name': b'userfile', b'filename': b'corsica_from_space_small.jpg'}), b'CONTENT_TYPE': (b'image/jpeg', {})}, 306, 65505, b'fixture/corsica_from_space_small.jpg')]),
            )

        for ((filename,boundary),newheaders_expected) in files:
            print("filename",filename)
            positions=atpic.getindata.multipart_parse_disk(boundary,filename)
            print("positions",positions)
            headers=atpic.getindata.multipart_get_the_headers(boundary,filename,positions)
            print("headers",headers)
            newheaders=atpic.getindata.multipart_extract_values(headers,filename)
            print('XXX', newheaders)
            i=0
            for newheader in newheaders:
                newheader_expected=newheaders_expected[i]
                i=i+1
                self.assertEqual(newheader[:3],newheader_expected[:3])
                self.assertEqual(True,filecmp.cmp(newheader[3],newheader_expected[3]))

    def test_get_indata(self):

        environs=(
            (
                {
                    b'REQUEST_METHOD':b'POST',
                    b'CONTENT_TYPE':b'application/x-www-form-urlencoded',
                    b'wsgi.input':io.BytesIO(b"first=alex&last=madon")
                    },
                [(b'first', False, b'alex'), (b'last', False, b'madon')]


                ),
            # b'group1=Cheese&food=%C3%A9t%C3%A9&food=automne&toppings=mushrooms&toppings=greenpeppers&toppings=onions'
            (
                {
                    b'REQUEST_METHOD':b'POST',
                    b'CONTENT_TYPE':b'application/x-www-form-urlencoded',
                    b'wsgi.input':io.BytesIO(b'group1=Cheese&food=%C3%A9t%C3%A9&food=automne&toppings=mushrooms&toppings=greenpeppers&toppings=onions')
                    },
                [(b'group1', False, b'Cheese'), (b'food', False, b'\xc3\xa9t\xc3\xa9'), (b'food', False, b'automne'), (b'toppings', False, b'mushrooms'), (b'toppings', False, b'greenpeppers'), (b'toppings', False, b'onions')]


                ),
            (
                {
                    b'REQUEST_METHOD':b'POST',
                    b'CONTENT_TYPE': b'multipart/form-data; boundary=---------------------------17286521591893302557554318847',
                    b'wsgi.input':open('fixture/forms_multipart_utf8','rb'),
                    },
                [(b'group1', False, b'Butter'), (b'food', False, b'\xc3\xa9t\xc3\xa9'), (b'food', False, b'automne'), (b'food', False, b'hiver'), (b'toppings', False, b'greenpeppers'), (b'toppings', False, b'onions'), (b'toppings', False, b'tomatoes')]
                
                ),
            (

                # {b'food': ['été'.encode('utf8'), b'automne', b'hiver'], b'toppings': [b'greenpeppers', b'onions', b'tomatoes'], b'group1': [b'Butter']},
                
                {
                    b'REQUEST_METHOD':b'POST',
                    b'CONTENT_TYPE': b'image/jpeg',
                    b'wsgi.input':open('fixture/corsica_from_space_small.jpg','rb'),
                    },
                [(b'contentypeother', True, (b'/tmp/atup1kep2t', b'', b'image/jpeg'))]
                ),
            (
                {
                    b'REQUEST_METHOD':b'POST',
                    b'CONTENT_TYPE': b'image/jpeg',
                    b'HTTP_SLUG':b'slug_corsica_from_space_small.jpg', # see picassa/atom
                    b'wsgi.input':open('fixture/corsica_from_space_small.jpg','rb'),
                    },
                [(b'contentypeother', True, (b'/tmp/atuphzarcy', b'slug_corsica_from_space_small.jpg', b'image/jpeg'))]
                ),



            (
                {
                    b'REQUEST_METHOD':b'POST',
                    b'CONTENT_TYPE':b'application/json',
                    b'wsgi.input':io.BytesIO(b'[["first","alex"],["last","madon"]]')
                    },
                [(b'first', False, b'alex'), (b'last', False, b'madon')]


                ),



            
            )
        j=0
        for (environ,alist_ex) in environs:
            j=j+1
            print("\n\n\n\n\n++++++++++++++++++++++++++",j,"++++++++++++++++++++++++++++++")
            alist=atpic.getindata.get_indata(environ)
            print("XXX alist=",alist)
            i=0
            for (aname,isfile,avalue) in alist:
                (aname_ex,isfile_ex,avalue_ex)=alist_ex[i]
                i=i+1
                if not isfile:
                    self.assertEqual(aname,aname_ex)
                    self.assertEqual(avalue,avalue_ex)
                else:
                    self.assertEqual(avalue[1:],avalue_ex[1:])
            environ[b'wsgi.input'].close()
                

    def NOtest_get_indata_error(self):

        environs=(

            
            (
                (
                    {
                        b'REQUEST_METHOD':b'POST',
                        b'CONTENT_TYPE': b'multipart/related; boundary="END_OF_PART"',
                        b'wsgi.input':open('fixture/google_picassa_atom1','rb'),
                        },
                    {},
                    [(b'/tmp/atup_RtElk', b'slug_corsica_from_space_small.jpg', b'image/jpeg')]
                    
                    ),
                )

            )
        for (environ,indata2,infiles2) in environs:
            self.assertRaises(Exception,atpic.getindata.get_indata,environ,None)
            environ[b'wsgi.input'].close()

if __name__=="__main__":
    unittest.main()
