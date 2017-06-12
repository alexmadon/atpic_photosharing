#!/usr/bin/python3
# ALTER TABLE _user_gallery_pic RENAME COLUMN _dateexif TO _datestoreexif;



for col in ['make','model','aperture','exposuretime','focallength','meteringmode','flash','whitebalance','exposuremode','sensingmethod','datetimeoriginal','datetimedigitized']:
    print('ALTER TABLE _user_gallery_pic RENAME COLUMN _',col,' TO _exif',col,';',sep='')



for col in ['lat','lon']:
    print('ALTER TABLE _user_gallery_pic RENAME COLUMN _',col,' TO _exifgps',col,';',sep='')
