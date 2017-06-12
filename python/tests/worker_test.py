#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import urllib.parse
import io



import atpic.worker
import atpic.xmlob
import atpic.xplo



class worker_test(unittest.TestCase):
    """USER legacy urls"""

    def test_set_sqldataerror(self):
        inputs=[
            ({},{b'msg': b'ERROR:  duplicate key value violates unique constraint "_user__u_login"\nDETAIL:  Key (_login)=(alexmadon3) already exists.\n', b'sqlstate': b'23505', b'primary': b'duplicate key value violates unique constraint "_user__u_login"', b'hint': None}),
        ]
        for (dic,ainput) in inputs:
            res=atpic.worker.set_sqldataerror({},ainput)
            print(res)




    def NOtest_what_needed(self):
        inputs=(
            ([(b'atpiccom', None)],[(b'robots.txt', None)],[b'get'], {},b'xhtml',(False, False, False)),

            ([(b'uname', b'alex')],[(b'treesearch', b'/italia2006')],[b'get'],{},b'xml',(True, False, False)),
            ([(b'uname', b'alex')],[(b'treesearch', b'/italia2006')],[b'get'],{b'QUERY_STRING': b'rank=10'},b'xml',(True, False, False)),
            ([(b'uname', b'alex')],[(b'tree', b'/italia2006')],[b'get'],{b'QUERY_STRING': b'rank=10'},b'xml',(True, False, False)),


        )
        for (hxplo,pxplo,actions,environ,aformat,expect) in inputs:
            res=atpic.worker.what_needed(atpic.xplo.Xplo(hxplo),atpic.xplo.Xplo(pxplo),actions,environ,aformat)
            print(res)
            self.assertEqual(res,expect)

    def NOtest_get_blog_solrquerynav(self):
        tests=(
            ({'uname': 'alex', 'userid': 1},"http://localhost:8983/solr/select?q=user:1&group=true&group.field=useryear"),
            ({'uname': 'alex', 'userid': 1, 'year': '2003'},"http://localhost:8983/solr/select?q=useryear:12003&group=true&group.field=useryearmonth"),
            ({'uname': 'alex', 'month': '12', 'userid': 1, 'year': '2003'},"http://localhost:8983/solr/select?q=useryearmonth:1200312&group=true&group.field=useryearmonthday&sort=useryearmonthday+desc"),
            ({'uname': 'alex', 'month': '12', 'userid': 1, 'day': '31', 'year': '2003'},""),
            )

        for adic,result in tests:
            res=atpic.worker.get_blog_solrquerynav(adic,None)
            self.assertEqual(res,result)






    def NOtest_get_blog_solrquerydata(self):
        tests=(
            ({'uname': 'alex', 'userid': 1},"http://localhost:8983/solr/select?q=user:1"),
            ({'uname': 'alex', 'userid': 1, 'year': '2003'},"http://localhost:8983/solr/select?q=useryear:12003"),
            ({'uname': 'alex', 'month': '12', 'userid': 1, 'year': '2003'},"http://localhost:8983/solr/select?q=useryearmonth:1200312&sort=useryearmonthday+desc"),
            ({'uname': 'alex', 'month': '12', 'userid': 1, 'day': '31', 'year': '2003'},"http://localhost:8983/solr/select?q=useryearmonthday:120031231&sort=useryearmonthday+desc"),
            )

        for adic,result in tests:
            res=atpic.worker.get_blog_solrquerydata(adic,None)
            self.assertEqual(res,result)



    def NOtest_get_tree_depth(self):
        tests=[
            ('/',0),
            ('/france',1),
            ('/france/',1),
            ('/france/paris',2),
            ('/france/paris/',2),
            ]
        for (path,depth_expected) in tests:
            res=atpic.worker.get_tree_depth(path,None)
            self.assertEqual(res,depth_expected)

    def NOtest_xmlo(self):
        xmlo=atpic.xmlob.Xmlo()
        xmlo.error_append("this is an error")
        # val=xmlo.getvalue()
        # print("xmlo=",val)















    def NOtest_get_path(self):
        paths=(
            ([],[(b'chapter',None)],[b'get'],b'atpic.faa',1,b'10',b'http://atpic.faa/chapter/10'),
            ([],[(b'chapter',b'1')],[b'get'],b'atpic.faa',1,b'1',b'http://atpic.faa/chapter/1'),
            ([],[(b'chapter',b'1'), (b'section',None)],[b'get'],b'atpic.faa',2,b'11',b'http://atpic.faa/chapter/1/section/11'),
            ([],[(b'chapter',b'1'), (b'section',b'222')],[b'get'],b'atpic.faa',2,b'222',b'http://atpic.faa/chapter/1/section/222'),
            ([],[(b'user',b'1'),(b'gallery', b'222'),(b'pic', b'333'),(b'comment', b'444')],[b'get'],b'alex.atpic.faa',1,b'1',b'http://atpic.faa/user/1'),
            ([],[(b'user',b'1'),(b'gallery', b'222'),(b'pic', b'333'),(b'comment', b'444')],[b'get'],b'alex.atpic.faa',1,b'1',b'http://atpic.faa/user/1'),
            ([],[(b'user',b'1'),(b'gallery', b'222'),(b'pic', b'333'),(b'comment', b'444')],[b'get'],b'alex.atpic.faa',2,b'222',b'http://alex.atpic.faa/gallery/222'),
            ([],[(b'user',b'1'),(b'gallery', b'222'),(b'pic', b'333'),(b'comment', b'444')],[b'get'],b'alex.atpic.faa',3,b'333',b'http://alex.atpic.faa/gallery/222/pic/333'),
            ([],[(b'user',b'1'),(b'gallery', b'222'),(b'pic', b'333'),(b'comment', b'444')],[b'get'],b'alex.atpic.faa',4,b'444',b'http://alex.atpic.faa/gallery/222/pic/333/comment/444'),
            ([],[(b'user',b'1'),(b'gallery', b'222'),(b'pic', b'333')],[b'get'],b'alex.atpic.faa',1,b'1',b'http://atpic.faa/user/1'),
            ([],[(b'user',b'1'),(b'gallery', b'222'),(b'pic', b'333')],[b'get'],b'alex.atpic.faa',2,b'222',b'http://alex.atpic.faa/gallery/222'),
            ([],[(b'user',b'1'),(b'gallery', b'222'),(b'pic', b'333')],[b'get'],b'alex.atpic.faa',3,b'333',b'http://alex.atpic.faa/gallery/222/pic/333'),
            ([],[(b'user',b'1'),(b'gallery', b'222'),(b'pic', b'333')],[b'get'],b'alex.atpic.faa',1,b'1',b'http://atpic.faa/user/1'),
            ([],[(b'user',b'1'),(b'gallery', b'222'),(b'pic', b'333')],[b'get'],b'alex.atpic.faa',2,b'222',b'http://alex.atpic.faa/gallery/222'),
            ([],[(b'user',b'1'),(b'gallery', b'222'),(b'pic', b'333')],[b'get'],b'alex.atpic.faa',3,b'333',b'http://alex.atpic.faa/gallery/222/pic/333'),
            ([],[(b'user',b'1'),(b'gallery',None)],[b'get'],b'alex.atpic.faa',1,b'1',b'http://atpic.faa/user/1'),
            ([],[(b'user',b'1'),(b'gallery',None)],[b'get'],b'alex.atpic.faa',2,b'222',b'http://alex.atpic.faa/gallery/222'),
            ([],[(b'user','1')],[b'get'],b'atpic.faa',1,b'1',b'http://atpic.faa/user/1'),
            ([],[(b'user',None)],[b'get'],b'atpic.faa',1,b'9',b'http://atpic.faa/user/9'),

            ([(b'uname', 'alex')],[(b'user',b'1'), (b'g', None)],[b'get'],b'alex.atpic.faa',1,b'1',b'http://atpic.faa/user/1'),
            ([(b'uname', 'alex')],[(b'user',b'1'), (b'g', None)],[b'get'],b'alex.atpic.faa',2,b'222',b'http://alex.atpic.faa/gallery/222'),
            ([(b'uname', 'alex')],[(b'user',b'1'), (b'gallery', b'222'), (b'g', None)],[b'get'],b'alex.atpic.faa',1,b'1',b'http://atpic.faa/user/1'),
            ([(b'uname', 'alex')],[(b'user',b'1'), (b'gallery', b'222'), (b'g', None)],[b'get'],b'alex.atpic.faa',2,b'222',b'http://alex.atpic.faa/gallery/222'),
            ([(b'uname', 'alex')],[(b'user',b'1'), (b'gallery', b'222'), (b'g', None)],[b'get'],b'alex.atpic.faa',3,b'1035',b'http://alex.atpic.faa/gallery/1035'),
            
            ([(b'uname', 'alex')],[(b'user',b'1'), (b'gallery', b'222'), (b'gallery', None)],[b'get'],b'alex.atpic.faa',3,b'7699',b'http://alex.atpic.faa/gallery/7699'),


            ([(b'uname', 'alex')],[(b'user',b'1'), (b'gallery', b'1'), (b'path', None)],[b'get'],b'alex.atpic.faa',3,b'48542',b'http://alex.atpic.faa/gallery/48542'),


            )
        i=0
        for path in paths:
            i=i+1
            print('=========== %s ==========' % i)
            environ={}
            line={}
            (hxplo,pxplo,actions,environ[b'HTTP_HOST'],depth,line[b'id'],apath)=path
            hxplo=atpic.xplo.Xplo(hxplo)
            pxplo=atpic.xplo.Xplo(pxplo)
            apath_expected=atpic.worker.set_path(hxplo,pxplo,actions,environ,depth,line)

            self.assertEqual(apath,apath_expected)














    def NOtest_set_pic_urls(self):
        paths=(
            ([],[(b'user',b'1'),(b'gallery', b'222'),(b'pic', b'333'),(b'comment', b'444')],[b'get'],b'10.99.99.99',3,b'333',b'http://alex.atpic.faa/gallery/222/pic/333'),
            ([],[(b'user',b'1'),(b'gallery', b'222'),(b'pic', b'333'),(b'comment', b'444')],[b'get'],b'10.99.99.99',4,b'444',b'http://alex.atpic.faa/gallery/222/pic/333/comment/444'),

            )
        i=0
        for path in paths:
            i=i+1
            print('=========== %s ==========' % i)
            environ={}
            line={}
            (hxplo,pxplo,actions,environ[b'SERVER_ADDR'],depth,line[b'id'],apath)=path
            hxplo=atpic.xplo.Xplo(hxplo)
            pxplo=atpic.xplo.Xplo(pxplo)
            apath_expected=atpic.worker.set_pic_urls(hxplo,pxplo,actions,environ,depth,line)

            # self.assertEqual(apath,apath_expected)







    def NOtest_xslt(self):

            output_xml="""<ok><get><get><USER url="http://atpic.faa/user/1"><rows>0</rows><synced></synced><css>1</css><lang>fr</lang><login>alexmadon</login><usage></usage><template>0</template><id>1</id><datelast></datelast><thestyleid>1</thestyleid><size_allowed></size_allowed><storeto></storeto><servername>user6.atpic.com</servername><email>alex@example.foo</email><servershort>alex</servershort><serverip>46.4.24.136</serverip><cols>0</cols><text>a &amp;b</text><password>removed</password><title></title><counter>15396</counter><mount>/hdc1</mount><storefrom>12</storefrom><datefirst></datefirst><name>Alex M</name><Gallery url="http://alex.atpic.faa/gallery"><gallery url="http://alex.atpic.faa/gallery/1"><rows>0</rows><file></file><skin_pic>0</skin_pic><priority></priority><css_gallery>2</css_gallery><css_pic>2</css_pic><id>1</id><mode>b</mode><datelast>2008-09-02 15:24:22.036494</datelast><template_pic>0</template_pic><bgcolor></bgcolor><style>2</style><cols>4</cols><secret>0</secret><text>Some macro photos I took with my powershot.</text><title>Macro</title><lon></lon><fgcolor></fgcolor><counter>4744</counter><lat></lat><datefirst>2004-02-11 00:00:00</datefirst><template_gallery>0</template_gallery><dir>3</dir><isroot>n</isroot><skin_gallery>0</skin_gallery><user>1</user></gallery><gallery url="http://alex.atpic.faa/gallery/3"><rows>0</rows><file>avignon</file><skin_pic>0</skin_pic><priority></priority><css_gallery>13,0</css_gallery><css_pic>13</css_pic><id>3</id><mode>b</mode><datelast>2007-03-24 15:23:32.152825</datelast><template_pic>0</template_pic><bgcolor></bgcolor><style>13</style><cols>4</cols><secret>0</secret><text></text><title>Avignon</title><lon>4.80789</lon><fgcolor></fgcolor><counter>212</counter><lat>43.9486</lat><datefirst>2004-02-14 00:00:00</datefirst><template_gallery>0</template_gallery><dir>48542</dir><isroot>n</isroot><skin_gallery>0</skin_gallery><user>1</user></gallery><gallery url="http://alex.atpic.faa/gallery/4"><rows>0</rows><file></file><skin_pic>0</skin_pic><priority></priority><css_gallery>1</css_gallery><css_pic>1</css_pic><id>4</id><mode>b</mode><datelast>2006-05-10 15:05:53.432652</datelast><template_pic>0</template_pic><bgcolor></bgcolor><style>1</style><cols>4</cols><secret>0</secret><text></text><title>Provence</title><lon></lon><fgcolor></fgcolor><counter>142</counter><lat></lat><datefirst>2004-02-14 00:00:00</datefirst><template_gallery>0</template_gallery><dir>48542</dir><isroot>n</isroot><skin_gallery>0</skin_gallery><user>1</user></gallery><gallery url="http://alex.atpic.faa/gallery/7"><rows>0</rows><file></file><skin_pic></skin_pic><priority>b</priority><css_gallery>9</css_gallery><css_pic>9</css_pic><id>7</id><mode>b</mode><datelast>2004-07-19 00:00:00</datelast><template_pic></template_pic><bgcolor></bgcolor><style>9</style><cols>4</cols><secret>0</secret><text></text><title>Paris</title><lon></lon><fgcolor></fgcolor><counter>12760</counter><lat></lat><datefirst>2004-04-13 00:00:00</datefirst><template_gallery></template_gallery><dir>128</dir><isroot>n</isroot><skin_gallery></skin_gallery><user>1</user></gallery><gallery url="http://alex.atpic.faa/gallery/128"><rows>0</rows><file>dama</file><skin_pic>0</skin_pic><priority></priority><css_gallery>1,0</css_gallery><css_pic>1</css_pic><id>128</id><mode>b</mode><datelast>2007-03-24 15:24:14.948101</datelast><template_pic>0</template_pic><bgcolor></bgcolor><style>1</style><cols>4</cols><secret>0</secret><text></text><title>Dama d'Italie</title><lon></lon><fgcolor></fgcolor><counter>149</counter><lat></lat><datefirst>2004-05-29 00:00:00</datefirst><template_gallery>0</template_gallery><dir>3</dir><isroot>n</isroot><skin_gallery>0</skin_gallery><user>1</user></gallery><gallery url="http://alex.atpic.faa/gallery/145"><rows>2</rows><file></file><skin_pic>0</skin_pic><priority>af</priority><css_gallery>13</css_gallery><css_pic>13</css_pic><id>145</id><mode>v</mode><datelast>2007-08-03 08:50:13.470244</datelast><template_pic>70</template_pic><bgcolor></bgcolor><style>13</style><cols>4</cols><secret>hdjinrdwzrfagfaoupgv</secret><text></text><title>Dama Indoor</title><lon></lon><fgcolor></fgcolor><counter>0</counter><lat></lat><datefirst>2004-06-02 00:00:00</datefirst><template_gallery>0</template_gallery><dir>48542</dir><isroot>n</isroot><skin_gallery>0</skin_gallery><user>1</user></gallery><gallery url="http://alex.atpic.faa/gallery/1035"><rows>0</rows><file></file><skin_pic>0</skin_pic><priority></priority><css_gallery>1</css_gallery><css_pic>1</css_pic><id>1035</id><mode>v</mode><datelast>2006-09-12 07:47:16.304847</datelast><template_pic>0</template_pic><bgcolor></bgcolor><style>1</style><cols>4</cols><secret>rltrnifuqlqmohflfbdm</secret><text>desc Kunst i Vrå 2006 ( PÅSKEN ) |</text><title>Kunst i Vrå 2006 ( PÅSKEN ) |</title><lon></lon><fgcolor></fgcolor><counter>0</counter><lat></lat><datefirst>2005-05-26 00:00:00</datefirst><template_gallery>0</template_gallery><dir>1</dir><isroot>n</isroot><skin_gallery>0</skin_gallery><user>1</user></gallery><gallery url="http://alex.atpic.faa/gallery/5317"><rows>0</rows><file></file><skin_pic>0</skin_pic><priority></priority><css_gallery>7</css_gallery><css_pic>0</css_pic><id>5317</id><mode>v</mode><datelast>2006-12-03 06:57:16.727245</datelast><template_pic>0</template_pic><bgcolor></bgcolor><style></style><cols>4</cols><secret>cbjeldohbbtvoiatpnfq</secret><text>test</text><title></title><lon></lon><fgcolor></fgcolor><counter>0</counter><lat></lat><datefirst>2006-05-10 15:11:14.862926</datefirst><template_gallery>3</template_gallery><dir>48542</dir><isroot>n</isroot><skin_gallery>0</skin_gallery><user>1</user></gallery><gallery url="http://alex.atpic.faa/gallery/7699"><rows>10</rows><file>matrimonio</file><skin_pic>0</skin_pic><priority></priority><css_gallery>0,0</css_gallery><css_pic>0</css_pic><id>7699</id><mode>b</mode><datelast>2006-12-25 10:12:31.216852</datelast><template_pic>0</template_pic><bgcolor></bgcolor><style></style><cols>4</cols><secret>0</secret><text>Morlupo, Italia 9Sett 2006</text><title>Matrimonio Gabriela e Christopher</title><lon>12.4976</lon><fgcolor></fgcolor><counter>245</counter><lat>42.1469</lat><datefirst>2006-09-12 15:06:30.385231</datefirst><template_gallery>0</template_gallery><dir>7700</dir><isroot>n</isroot><skin_gallery>0</skin_gallery><user>1</user></gallery><gallery url="http://alex.atpic.faa/gallery/7700"><rows>0</rows><file>italia2006</file><skin_pic>0</skin_pic><priority></priority><css_gallery>0</css_gallery><css_pic>0</css_pic><id>7700</id><mode>b</mode><datelast>2006-09-12 15:18:14.044062</datelast><template_pic>0</template_pic><bgcolor></bgcolor><style></style><cols>4</cols><secret>0</secret><text>Settembre 2006</text><title>Italia 2006</title><lon></lon><fgcolor></fgcolor><counter>192</counter><lat></lat><datefirst>2006-09-12 15:18:14.044062</datefirst><template_gallery>0</template_gallery><dir>48542</dir><isroot>n</isroot><skin_gallery>0</skin_gallery><user>1</user></gallery></Gallery></USER></get></get></ok>"""
            output_xsl=""
            output=atpic.worker.xslt_apply_ps(output_xsl,output_xml)
            print(output)

    def NOtest_convert_sqltime_xmltime(self):

        times=(
            (b'2004-02-12 11:52:15',b'2004-02-12T11:52:15.000000'),
            )
        for (sqltime,xmltime) in times:

            xmltime2=atpic.worker.convert_sqltime_xmltime(sqltime)
            print('FFFF',xmltime)
            self.assertEqual(xmltime,xmltime2)

    def NOtest_display_one(self):

        lines=(
            ({b'_rows': b'0', b'_synced': b'', b'_css': b'1', b'_lang': b'fr', b'_login': b'alexmadon', b'_usage': b'', b'_template': b'0', b'id': b'1', b'_datelast': b'', b'_thestyleid': b'1', b'_size_allowed': b'', b'_storeto': b'', b'_email': b'alex@example.foo', b'_servershort': b'alex', b'_cols': b'0', b'_text': b'a &amp;b', b'_password': b'passwdsalted', b'_title': b'', b'_counter': b'15396', b'_storefrom': b'12', b'_datefirst': b'', b'_name': b'Alex M'},
b'<rows>0</rows><synced></synced><css>1</css><lang>fr</lang><login>alexmadon</login><usage></usage><template>0</template><id>1</id><datelast></datelast><thestyleid>1</thestyleid><size_allowed></size_allowed><storeto></storeto><email>alex@example.foo</email><servershort>alex</servershort><cols>0</cols><text>a &amp;b</text><password>removed</password><title></title><counter>15396</counter><storefrom>12</storefrom><datefirst></datefirst><name>Alex M</name>'),
            ({b'_datemy': b''},b'<datemy></datemy>'),
            )
        for (adic,ares) in lines:
            xmlo=atpic.xmlob.Xmlo()
            
            nxmlo=atpic.worker.display_one_object(adic,xmlo)
            
            res=b''.join(nxmlo.data.content)
            print('XXXX',res)
            self.assertEqual(res,ares)

        pass

    def test_check_end_col(self):
        inputs=(
            (( 1 , [(b'user', None)] , [b'get'] ),True),
            (( 1 , [(b'user', b'1')] , [b'get'] ),False),
            (( 2 , [(b'user', b'1'), (b'wiki', b'/'), (b'revision', None)] , [b'get'] ),True),
            (( 2 , [(b'user', b'1'), (b'wiki', b'/'), (b'revision', b'1,2')] , [b'get'] ),True),
            (( 2 , [(b'user', b'1'), (b'wiki', b'/'), (b'revision', b'1')] , [b'get'] ),False),
            )
        i=0
        for (depth,pxplo,actions),expect in inputs:
            i=i+1
            print('endcol+++++++++++++++++++',i,'+++++++++++++++++++')
            pxplo=atpic.xplo.Xplo(pxplo)
            # print('VVV',(depth,pxplo,actions))
            res=atpic.worker.check_end_collection(depth,pxplo,actions)
            print('VVV',((depth,pxplo.list(),actions),res))
            self.assertEqual(res,expect)


    def NOtest_check_allowed_hvalues(self):
        inputs=(
            ([(b'uname', b'alex')] , [(b'gallery', b'1'), (b'pic', None)], b''),
            ([(b'uname', b'alex')] , [(b'gallery', b'1'), (b'pic', b'1')], b''),
            ([(b'uname', b'alex')] , [(b'below', b'/')], b''),
            ([(b'uname', b'alex')] , [(b'belownav', b'/')],b''),

            ([(b'uname', b'alex')] , [(b'gallery', b'1'), (b'pic', b'1put')],b"value '1put' is not valid for key 'pic'"),
            ([(b'uname', b'alex')] , [(b'gallery', b'1dum'), (b'pic', b'1')],b"value '1dum' is not valid for key 'gallery'"),


            )
        for (hp,pp,expect) in inputs:
            hxplo=atpic.xplo.Xplo(hp)
            pxplo=atpic.xplo.Xplo(pp)
            res=atpic.worker.check_allowed_hvalues_basic(hxplo,pxplo)
            self.assertEqual(res,expect)

    def NOtest_actions_transform(self):
        inputs=(
            (True,[b'get',b'put'],[b'get',b'put']),
            (True,[b'post',b'put'],[b'get',b'put']),
            (True,[b'put'],[b'get',b'put']),
            (True,[b'get',b'post'],[b'get',b'post']),
            (True,[b'post',b'post'],[b'get',b'post']),
            (True,[b'post'],[b'get',b'post']),

            (False,[b'get',b'put'],[b'get',b'put']),
            (False,[b'post',b'put'],[b'post',b'put']),
            (False,[b'put'],[b'put']),
            (False,[b'get',b'post'],[b'get',b'post']),
            (False,[b'post',b'post'],[b'post',b'post']),
            (False,[b'post'],[b'post']),


            )
        for (haserror,actions,expect) in inputs:
            res=atpic.worker.actions_transform(actions,haserror)
            self.assertEqual(res,expect)

    def NOtest_check_allowed_hvalues_basic(self):
        inputs=(
            ([(b'atpiccom', None)] , [(b'faq', b'/')], b''),
            ([(b'uname', b'alex')] , [(b'gallery', b'1')], b''),
            ([(b'uname', b'alex')] , [(b'gallery', b'1dum')], b"value '1dum' is not valid for key 'gallery'"),
            )
        for (hxplo1,pxplo1,expect) in inputs:
            hxplo=atpic.xplo.Xplo(hxplo1)
            pxplo=atpic.xplo.Xplo(pxplo1)
            res=atpic.worker.check_allowed_hvalues_basic(hxplo,pxplo)
            self.assertEqual(res,expect)

    def test_data_hide(self):
        inputs=(
            (b'_password',[],[],[],True),
            (b'_dummy',[],[],[],False),
            )
        for (key,hxplo1,pxplo1,actions,expect) in inputs:
            hxplo=atpic.xplo.Xplo(hxplo1)
            pxplo=atpic.xplo.Xplo(pxplo1)
            res=atpic.worker.data_hide(key,hxplo,pxplo,actions)
            self.assertEqual(res,expect)


if __name__=="__main__":
    unittest.main()
