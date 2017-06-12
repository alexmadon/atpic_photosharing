import pyexiv2


# $fields["make"]             ="'".sqlclean(reset_ifnot_utf8(substr(# $exif["IFD0"]["Make"],0,127)))."'";
# $fields["model"]            ="'".sqlclean(reset_ifnot_utf8(substr(# $exif["IFD0"]["Model"],0,127)))."'";
# $fields["aperture"]         ="'".sqlclean(reset_ifnot_utf8(substr(# $exif["COMPUTED"]["ApertureFNumber"],0,127)))."'";
# $fields["exposuretime"]     ="'".sqlclean(reset_ifnot_utf8(substr(# $exif["EXIF"]["ExposureTime"],0,127)))."'";
# $fields["focallength"]      ="'".sqlclean(reset_ifnot_utf8(substr(# $exif["EXIF"]["FocalLength"],0,127)))."'";
# $fields["MeteringMode"]     ="'".sqlclean(reset_ifnot_utf8(substr(# $exif["EXIF"]["MeteringMode"],0,127)))."'";
# $fields["Flash"]            ="'".sqlclean(reset_ifnot_utf8(substr(# $exif["EXIF"]["Flash"],0,127)))."'";
# $fields["WhiteBalance"]     ="'".sqlclean(reset_ifnot_utf8(substr(# $exif["EXIF"]["WhiteBalance"],0,127)))."'";
# $fields["ExposureMode"]     ="'".sqlclean(reset_ifnot_utf8(substr(# $exif["EXIF"]["ExposureMode"],0,127)))."'";
# $fields["SensingMethod"]    ="'".sqlclean(reset_ifnot_utf8(substr(# $exif["EXIF"]["SensingMethod"],0,127)))."'";
# $fields["DateTimeOriginal"] ="'".sqlclean(reset_ifnot_utf8(substr(# $exif["EXIF"]["DateTimeOriginal"],0,127)))."'";
# $fields["DateTimeDigitized"]="'".sqlclean(reset_ifnot_utf8(substr(# $exif["EXIF"]["DateTimeDigitized"],0,127)))."'";

# $fields["ISOSpeedRatings"]  ="'".sqlclean(reset_ifnot_utf8(substr(# $exif["EXIF"]["ISOSpeedRatings"],0,127)))."'";



#GEO
# 'Exif.GPSInfo.GPSLatitudeRef', 'Exif.GPSInfo.GPSLatitude', 'Exif.GPSInfo.GPSLongitudeRef', 'Exif.GPSInfo.GPSLongitude', 'Exif.GPSInfo.GPSAltitudeRef', 'Exif.GPSInfo.GPSAltitude'

# will return XML as file operation are done on a remote node


def exif_atpic(file):
    """lists all the exif fields needed for atpic"""
    image = pyexiv2.Image(file)
    image.readMetadata()
    xmllist=[]
    atpickeys=[
        "Exif.Image.Make",
        "Exif.Image.Model",
        "Exif.Photo.FNumber",
        "Exif.Photo.ExposureTime",
        "Exif.Photo.FocalLength",
        "Exif.Photo.MeteringMode",
        "Exif.Photo.Flash",
        "Exif.Photo.WhiteBalance",
        "Exif.Photo.ExposureMode",
        "Exif.Photo.SensingMethod",
        "Exif.Photo.DateTimeOriginal",
        "Exif.Photo.DateTimeDigitized"
        ]
    # also interesting:
    # Exif.Photo.FocalLengthIn35mmFilm on Nikon
    xmllist.append("<atpicdata>\n")
    for key in atpickeys:
        # if image.has_key(key):
        if key in image.exifKeys():
            xmllist.append("<%s>" % key)
            xmllist.append("%s" % image.interpretedExifValue(key)) # or image[key]
            xmllist.append("</%s>\n" % key)

    # imageDateTime = image['Exif.Image.DateTime']
    # xml=imageDateTime.strftime('%A %d %B %Y, %H:%M:%S')
    
    imageDateTime = image['Exif.Image.DateTime']
    xml=imageDateTime.strftime('%A %d %B %Y, %H:%M:%S')
    
    # print image.iptcKeys()
    # http://www.melaneum.com/blog/wp-content/uploads/2008/04/jpegtokml.py
    # http://code.google.com/p/picasapush/source/browse/trunk/picturetags.py?r=246
    try:
        # longitude
        lonRational=image['Exif.GPSInfo.GPSLongitude']
        lon=eval('0.0+'+str(lonRational[0])+'+1/60.*'+str(lonRational[1])+'+1/3600.*'+str(lonRational[2]))
        ref = image['Exif.GPSInfo.GPSLongitudeRef']
        if ref == 'W' :
            lon = -lon
        # latitude
        latRational=image['Exif.GPSInfo.GPSLatitude']
        lat=eval('0.0+'+str(latRational[0])+'+1/60.*'+str(latRational[1])+'+1/3600.*'+str(latRational[2]))
        ref = image['Exif.GPSInfo.GPSLatitudeRef']
        if ref == 'S' :
            lat = -lat
        xmllist.append("<lon>%s</long>" % lon)
        xmllist.append("<lat>%s</lat>" % lat)

    except (IndexError,TypeError,KeyError):
        pass

    # for key in image.exifKeys():
    #     if key.find('GPS') != -1:
    #         print key, ':', image[key], ':', image.interpretedExifValue(key)

    xmllist.append("</atpicdata>\n")

    return "".join(xmllist)



def exif_all(file):
    """lists all the exif fields
    Returns a valid XML."""
    image = pyexiv2.Image(file)
    image.readMetadata()
    xmllist=[]
    xmllist.append("<data>\n")
    # print type(image.exifKeys())

    # may need to sanitize input fields
    for key in image.exifKeys():
        xmllist.append("<%s>" % key)
        xmllist.append("%s" %image.interpretedExifValue(key))
        xmllist.append("</%s>\n" % key)
    # could concatenate with "+" the two exif and IPTC but no interpreted function for iptc
    for key in image.iptcKeys():
        xmllist.append("<%s>" % key)
        xmllist.append("%s" % image[key])
        xmllist.append("</%s>\n" % key)

    xmllist.append("</data>")

    return "".join(xmllist)




