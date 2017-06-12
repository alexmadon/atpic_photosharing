#!/usr/bin/python3
# mimetypes.guess_all_extensions('image/jpeg')
import unittest

import atpic.processinfiles




mime_list=(
    (b'image/jpeg',b'jpg'),
    (b'image/x-canon-crw',b'crw'),
    (b'image/x-canon-cr2',b'cr2'),
    (b'image/x-fujifilm-raf',b'raf'),
    (b'image/x-minolta-mrw',b'mrw'),
    (b'image/x-nikon-nef',b'nef'),
    (b'image/x-olympus-orf',b'orf'),
    (b'image/x-pentax-pef',b'pef'),
    (b'image/x-sigma-x3f',b'x3f'),
    (b'image/x-sony-arw',b'arw'),
    (b'video/3gpp2',b'3g2'),
    (b'video/3gpp',b'3gp'),
    (b'video/x-m4v',b'm4v'),
    (b'video/quicktime',b'mov'),
    (b'video/mpeg',b'mpg'),
    (b'video/mp4',b'mp4'),
)

class worker_test(unittest.TestCase):
    """USER legacy urls"""

    def test_mime(self):
        for (mime,ext) in mime_list:
            ext_calc=atpic.processinfiles.mime2extension(mime)
            self.assertEqual(ext,ext_calc)


    def test_get_goodfilename(self):
        tests=(
            ((b'999',b'jpg',b''),b'999.jpg'),
            ((b'999',b'jpg',b'myslug.jpeg'),b'myslug.jpeg'),

            ((b'2090766',b'jpg',b'/tmp/atuprnblc1'),b'2090766.jpg'),


            )


        i=0
        for ((pid,extension,infilename),goodfilename_ex) in tests:
            i=i+1
            print('+++++++++++',i,'++++++++++++++++')
            goodfilename=atpic.processinfiles.get_goodfilename(pid,extension,infilename)
            
            self.assertEqual(goodfilename,goodfilename_ex)


    def test_update_xmlo(self):
        inputs=[(b'<USER url="http://atpic.faa/user/1"><rows>0</rows><synced></synced><css>1</css><lang>fr</lang><login>alexmadon</login><usage></usage><template>0</template><id>1</id><datelast></datelast><thestyleid>1</thestyleid><size_allowed></size_allowed><storeto></storeto><servername>user6.atpic.com</servername><email>alex@example.foo</email><servershort>alex</servershort><serverip>46.4.24.136</serverip><cols>0</cols><text>a &amp;b</text><password>salted</password><title></title><counter>15396</counter><mount>/hdc1</mount><storefrom>12</storefrom><datefirst>2012-05-01T11:50:32.995023</datefirst><name>Alex M</name><GALLERY url="http://alex.atpic.faa/gallery/1"><rows>0</rows><file></file><datemtime>2004-02-11T00:00:00.000000</datemtime><skin_pic>0</skin_pic><priority></priority><css_gallery>2</css_gallery><css_pic>2</css_pic><id>1</id><mode>b</mode><datelast>2008-09-02T15:24:22.036494</datelast><template_pic>0</template_pic><bgcolor></bgcolor><style>2</style><cols>4</cols><secret></secret><text>Some macro photos I took with my powershot.</text><title>Macro</title><lon></lon><fgcolor></fgcolor><counter>4744</counter><lat></lat><datefirst>2004-02-11T00:00:00.000000</datefirst><template_gallery>0</template_gallery><dir>3</dir><isroot>n</isroot><skin_gallery>0</skin_gallery><user>1</user><pic url="http://alex.atpic.faa/gallery/1/pic/2090757" fasturl="http://127.0.0.1/u1/1//2090757"><mimetype_exiftool></mimetype_exiftool><exifmodel></exifmodel><datestore350>2012-07-01T10:37:18.972418</datestore350><datestore160>2012-07-01T10:37:18.972418</datestore160><exifdatetimedigitized></exifdatetimedigitized><datestore600>2012-07-01T10:37:18.972418</datestore600><priority></priority><exiffocallength></exiffocallength><link></link><sizeexif>0</sizeexif><datemtime>2012-07-01T10:37:18.972418</datemtime><exifaperture></exifaperture><id>2090757</id><exifdatetimeoriginal></exifdatetimeoriginal><size1024>0</size1024><exifgpslon></exifgpslon><exifflash></exifflash><notpop>0</notpop><datestore70>2012-07-01T10:37:18.972418</datestore70><exifwhitebalance></exifwhitebalance><datelast>2012-07-01T10:37:18.972418</datelast><gallery>1</gallery><sizeb>0</sizeb><mimetype_magic></mimetype_magic><exifexposuremode></exifexposuremode><datestore1024>2012-07-01T10:37:18.972418</datestore1024><extension></extension><bgcolor></bgcolor><mimesubtype_magic></mimesubtype_magic><done></done><height></height><exifmeteringmode></exifmeteringmode><exifsensingmethod></exifsensingmethod><exifmake></exifmake><mimesubtype_exiftool></mimesubtype_exiftool><originalname></originalname><text></text><reviewed>0</reviewed><title></title><size70>0</size70><fgcolor></fgcolor><counter>0</counter><size0>0</size0><user>1</user><exifexposuretime></exifexposuretime><datestore0>2012-07-01T10:37:18.972418</datestore0><datestoreexif></datestoreexif><width></width><datefirst>2012-07-01T10:37:18.972418</datefirst><datetimeoriginalsql></datetimeoriginalsql><size160>0</size160><revaccepted>0</revaccepted><size350>0</size350><size600>0</size600><isospeedratings></isospeedratings><exifgpslat></exifgpslat></pic></GALLERY></USER>', b'197814', b'jpg', b'image', b'jpeg', b'/somepath',b'AGOOD.JPG',b'a',b'1111',b'<USER url="http://atpic.faa/user/1"><rows>0</rows><synced/><css>1</css><lang>fr</lang><login>alexmadon</login><usage/><template>0</template><id>1</id><datelast/><thestyleid>1</thestyleid><size_allowed/><storeto/><servername>user6.atpic.com</servername><email>alex@example.foo</email><servershort>alex</servershort><serverip>46.4.24.136</serverip><cols>0</cols><text>a &amp;b</text><password>salted</password><title/><counter>15396</counter><mount>/hdc1</mount><storefrom>12</storefrom><datefirst>2012-05-01T11:50:32.995023</datefirst><name>Alex M</name><GALLERY url="http://alex.atpic.faa/gallery/1"><rows>0</rows><file/><datemtime>2004-02-11T00:00:00.000000</datemtime><skin_pic>0</skin_pic><priority/><css_gallery>2</css_gallery><css_pic>2</css_pic><id>1</id><mode>b</mode><datelast>2008-09-02T15:24:22.036494</datelast><template_pic>0</template_pic><bgcolor/><style>2</style><cols>4</cols><secret/><text>Some macro photos I took with my powershot.</text><title>Macro</title><lon/><fgcolor/><counter>4744</counter><lat/><datefirst>2004-02-11T00:00:00.000000</datefirst><template_gallery>0</template_gallery><dir>3</dir><isroot>n</isroot><skin_gallery>0</skin_gallery><user>1</user><pic url="http://alex.atpic.faa/gallery/1/pic/2090757" fasturl="http://127.0.0.1/u1/1//2090757"><mimetype_exiftool/><exifmodel/><datestore350>2012-07-01T10:37:18.972418</datestore350><datestore160>2012-07-01T10:37:18.972418</datestore160><exifdatetimedigitized/><datestore600>2012-07-01T10:37:18.972418</datestore600><priority/><exiffocallength/><link/><sizeexif>0</sizeexif><datemtime>2012-07-01T10:37:18.972418</datemtime><exifaperture/><id>2090757</id><exifdatetimeoriginal/><size1024>0</size1024><exifgpslon/><exifflash/><notpop>0</notpop><datestore70>2012-07-01T10:37:18.972418</datestore70><exifwhitebalance/><datelast>2012-07-01T10:37:18.972418</datelast><gallery>1</gallery><sizeb>0</sizeb><mimetype_magic>image</mimetype_magic><exifexposuremode/><datestore1024>2012-07-01T10:37:18.972418</datestore1024><extension>jpg</extension><bgcolor/><mimesubtype_magic>jpeg</mimesubtype_magic><done/><height/><exifmeteringmode/><exifsensingmethod/><exifmake/><mimesubtype_exiftool/><originalname>AGOOD.JPG</originalname><text/><reviewed>0</reviewed><title/><size70>0</size70><fgcolor/><counter>0</counter><size0>197814</size0><user>1</user><exifexposuretime/><datestore0>2012-07-01T10:37:18.972418</datestore0><datestoreexif/><width/><datefirst>2012-07-01T10:37:18.972418</datefirst><datetimeoriginalsql/><size160>0</size160><revaccepted>0</revaccepted><size350>0</size350><size600>0</size600><isospeedratings/><exifgpslat/><pathstore>aSCb1JiZscmUtlX1UJiypZw==.jpg</pathstore></pic></GALLERY></USER>'

)]

        for (xml_string,st_size,extension,mimetype_magic,mimesubtype_magic,pathstore,goodfilename,partition,pid,expected) in inputs:
            # print(xml_string,st_size,extension,mimetype_magic,mimesubtype_magic,goodfilename)

            newxml=atpic.processinfiles.update_xmlo(xml_string,st_size,extension,mimetype_magic,mimesubtype_magic,pathstore,goodfilename,partition,pid)
            # print(newxml)
            self.assertEqual(newxml,expected)


if __name__=="__main__":

    unittest.main()
