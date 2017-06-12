from lxml import etree
import xml.etree.ElementTree as petree
from xml.dom import minidom
import io
import atpic.log
# import logging

xx=atpic.log.setmod("INFO","xmlutils")




class XMLnotValid(Exception):
     pass

def get(xml_string,path):
     yy=atpic.log.setname(xx,'get')
     atpic.log.debug(yy,'input=',(xml_string,path))
     # xml_doc = etree.parse(io.StringIO(xml_string))
     xml_doc = etree.parse(io.BytesIO(xml_string))
     el=xml_doc.xpath(path)
     # print(dir(xml_doc))
     # print(el)
     # print(dir(el))
     val=el[0].text
     # print(dir(el[0]))
     if val:
          res=val.encode('utf8')
     else:
          res=b''
     atpic.log.debug(yy,'output=',res)
     return res


def get_exif(xml_string):
     # process the output of exiftool -X -l
     # to extract the paramters that needs to be stored in SQL
     # and that needs to be used ulater in processing

     # ********************** BEST to use COMPOSITE Tags ************
     # http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Composite.html
     # **************************************************

     """
 _width                 | integer                     | 
 _height                | integer                     | 
 _originalname          | character varying(127)      | 
 _priority              | character varying(63)       | 
 _exifmake              | character varying(127)      | 
 _exifmodel             | character varying(127)      | 
 _exifaperture          | character varying(127)      | 
 _exifexposuretime      | character varying(127)      | 
 _exiffocallength       | character varying(127)      | 
 _exifmeteringmode      | character varying(127)      | 
 _exifflash             | character varying(127)      | 
 _exifwhitebalance      | character varying(127)      | 
 _exifexposuremode      | character varying(127)      | 
 _exifsensingmethod     | character varying(127)      | 
 _exifdatetimeoriginal  | character varying(127)      | 
 _exifdatetimedigitized | character varying(127)      | 
 _exifgpslat            | real                        | 
 _exifgpslon            | real                        | 
     paths=[
         '/rdf:RDF/rdf:Description/File:ImageWidth/et:prt',
         '/rdf:RDF/rdf:Description/ImageHeight/et:prt',
         '/rdf:RDF/rdf:Description/IFD0:Make/et:prt',
         '/rdf:RDF/rdf:Description/IFD0:Model/et:prt',
         '/rdf:RDF/rdf:Description/ExifIFD:ApertureValue/et:prt',
         '/rdf:RDF/rdf:Description/ExifIFD:ExposureTime/et:prt',
         '/rdf:RDF/rdf:Description/ExifIFD:FocalLength/et:prt',
         '/rdf:RDF/rdf:Description/ExifIFD:Flash/et:prt',
         '/rdf:RDF/rdf:Description/ExifIFD:WhiteBalance/et:prt',
         '/rdf:RDF/rdf:Description/ExifIFD:ExposureMode/et:prt',
         '/rdf:RDF/rdf:Description/ExifIFD:DateTimeOriginal/et:prt',


          '/rdf:RDF/rdf:Description/System:FileSize/et:prt',
          # '/RDF/Description/FileSize/prt',
          ]
 """

     paths=[
          '/rdf:RDF/rdf:Description/File:MIMEType/et:prt',
          '/rdf:RDF/rdf:Description/Composite:ImageSize/et:prt', # used for nikon NEF to get the largest
          '/rdf:RDF/rdf:Description/Composite:Duration/et:val', # for videos
          '/rdf:RDF/rdf:Description/IFD0:Make/et:prt|/rdf:RDF/rdf:Description/SigmaRaw:Make/et:prt',
          '/rdf:RDF/rdf:Description/IFD0:Model/et:prt|/rdf:RDF/rdf:Description/SigmaRaw:Model/et:prt',

          '/rdf:RDF/rdf:Description/Composite:Aperture/et:prt', 

          # '/rdf:RDF/rdf:Description/ExifIFD:ApertureValue/et:prt',
          '/rdf:RDF/rdf:Description/ExifIFD:ExposureTime/et:val',
          '/rdf:RDF/rdf:Description/ExifIFD:FocalLength/et:val',
          '/rdf:RDF/rdf:Description/ExifIFD:Flash/et:val',
          '/rdf:RDF/rdf:Description/ExifIFD:WhiteBalance/et:val',
          '/rdf:RDF/rdf:Description/ExifIFD:ExposureMode/et:val',
          '/rdf:RDF/rdf:Description/ExifIFD:DateTimeOriginal/et:prt',
          '/rdf:RDF/rdf:Description/Composite:GPSLatitude/et:val',
          '/rdf:RDF/rdf:Description/Composite:GPSLongitude/et:val',

          ]
     namespaces={
          'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
          'et':'http://ns.exiftool.ca/1.0/',
          'et:toolkit':'Image::ExifTool 8.60',
          'ExifTool':'http://ns.exiftool.ca/ExifTool/1.0/',
          'System':'http://ns.exiftool.ca/File/System/1.0/',
          'File':'http://ns.exiftool.ca/File/1.0/',
          'IFD0':'http://ns.exiftool.ca/EXIF/IFD0/1.0/',
          'ExifIFD':'http://ns.exiftool.ca/EXIF/ExifIFD/1.0/',
          'IFD1':'http://ns.exiftool.ca/EXIF/IFD1/1.0/',
          'SubIFD1':'http://ns.exiftool.ca/EXIF/SubIFD1/1.0/',
          'Composite':'http://ns.exiftool.ca/Composite/1.0/',
          # special ones
          'CanonRaw':'http://ns.exiftool.ca/MakerNotes/CanonRaw/1.0/',
          'Canon':'http://ns.exiftool.ca/MakerNotes/Canon/1.0/',
          'SigmaRaw':'http://ns.exiftool.ca/SigmaRaw/SigmaRaw/1.0/',
          'Composite':'http://ns.exiftool.ca/Composite/1.0/',

          }
     return get_new_image_params_basic(xml_string,paths,namespaces)


def get_new_image_params(xml_string):
     paths=[
          '/USER/partition',
          '/USER/id',
          '/USER/GALLERY/id',
          '/USER/GALLERY/pic/id',
          ]
     namespaces={}
     return get_new_image_params_basic(xml_string,paths,namespaces)

def get_new_image_params_basic(xml_string,paths,namespaces):
     """
     The XML is the one expected on a image upload
     """
     yy=atpic.log.setname(xx,'get_new_image_params')
     atpic.log.debug(yy,'input=',xml_string)
     
     # xml_doc = etree.parse(io.StringIO(xml_string))
     xml_doc = etree.parse(io.BytesIO(xml_string))
     # print(xml_doc)
     results=[]
     for path in paths:
          try:
               atpic.log.debug(yy,'doing path=',path)
               el=xml_doc.xpath(path,namespaces=namespaces)
               val=el[0].text.encode('utf8')
               results.append(val)
               atpic.log.debug(yy,'elem22',el)
          except IndexError:
               atpic.log.debug(yy,'EXIF path empty',path)
               results.append(b'')


     res=tuple(results)
     atpic.log.debug(yy,'output=',res)

     return res

def set_virtualpxplo(hxplo,pxplo,uid):
    yy=atpic.log.setname(xx,'set_virtualpxplo')
    atpic.log.debug(yy,"input=",hxplo.list(),pxplo.list(),uid)
    # create a new path xplotded with 'user' prepended; NOT GOOD
    if hxplo.getmatrix(0,0) in [b'uname',b'pdns']:
        pxplo=atpic.xplo.Xplo([(b'user',uid),]+pxplo.list())
    atpic.log.debug(yy,"new pxplo",pxplo.list())
    return pxplo

def get_deepest_path(hxplo,pxplo,actions,uid):
     """
     In forms post processing, you need to know the path where to replace.
     """
     # pxplo=set_virtualpxplo(hxplo,pxplo,uid)

     yy=atpic.log.setname(xx,'get_deepest_path')
     atpic.log.debug(yy,'input==',(hxplo,pxplo,actions,uid))
     pxplo=atpic.xmlutils.set_virtualpxplo(hxplo,pxplo,uid)
     atpic.log.debug(yy,'newpxplo=',pxplo)
     keys=pxplo.keys()
     atpic.log.debug(yy,keys)
     atpic.log.debug(yy,"need to uppercase the first ones, this is read-write")
     newkeys=[]
     i=1
     for key in keys:
          if i<len(keys):
               newkeys.append(key.upper())
          else:
               newkeys.append(key)
          i=i+1
     atpic.log.debug(yy,'newkeys=',newkeys)

     path=b'/'.join(newkeys)
     atpic.log.debug(yy,path)
     path=b'/'+path
     atpic.log.debug(yy,'output=',path)
     return path

def replace_params(xml_string,basepath,anarray):
     """
     Replaces in a XML elements in anarray from the xpath base
     If more than one match, only update the first matched element
     If no match, then create an element with that value
     """
     yy=atpic.log.setname(xx,'replace_params')

     xml_doc = etree.parse(io.BytesIO(xml_string))
     for (key,value) in anarray.items():
          atpic.log.debug(yy,'(key,value)',(key,value))
          if isinstance(value, list):
               newvalue=value[0] # we accept arrays of lists, the take the first
               value=newvalue
          path=basepath+b'/'+key
          atpic.log.debug(yy,'path=',path)
          el=xml_doc.xpath(path)
          atpic.log.debug(yy,'res==',el)
          if len(el)>0:
               atpic.log.debug(yy,'non empty')
               el[0].text=value
          else:
               atpic.log.debug(yy,'empty list! will need to create an element')
               baseel=xml_doc.xpath(basepath)
               if len(baseel)>0:
                    newel=etree.SubElement(baseel[0], key)
                    newel.text=value
     # return the modified XML
          
     ss=etree.tostring(xml_doc)
     atpic.log.debug(yy,'will return',ss)
     return ss





