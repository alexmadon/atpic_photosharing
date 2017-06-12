#!/usr/bin/python3
import unittest
import atpic.coordinates

class coordinates_test(unittest.TestCase):
    """USER legacy urls"""
    

    def NOtest_idempotent_pack(self):
        inputs=(
            ((12,10),4),
            (((1<<4) - 1,0),4),
            # ((256,10),4),
            (((1<<5)-1,0),5),
            (((1<<6)-1,0),6),

            )
        i=0
        for ((lon,lat),wlen) in inputs:
            i=i+1 
            print('++++++++++++++++',i,'++++++++++++++++++')
            
            packed=atpic.coordinates.pack(lon,lat,wlen)
            (lon2,lat2)=atpic.coordinates.unpack(packed,wlen)
            self.assertEqual((lon,lat), (lon2,lat2))




    def NOtest_idempotent2_pack(self):
        
        for i in range(2,32):
            print('++++++++++++++++ i=',i,'++++++++++++++++++')
            lat=0
            lon=(1<<i) - 1
            for wlen in range(i,32):
                print('++++++++++++++++ i=',i,'wlen=',wlen,'++++++++++++++++++')
                packed=atpic.coordinates.pack(lon,lat,wlen)
                (lon2,lat2)=atpic.coordinates.unpack(packed,wlen)
                self.assertEqual((lon,lat), (lon2,lat2))


 
    def NOtest_pack(self):
        inputs=(
            ((15, 15), 4, -1) ,
            ((15, 0), 4, 85) ,
            ((7, 7), 3, 63) ,
            ((7, 0), 3, 21) ,
            ((447336, 8193228), 23, 46962533840096) ,
            )
        i=0
        for ((lon,lat),wlen,expect) in inputs:
            i=i+1
            print('++++++++++++++++',i,'++++++++++++++++++')
            res=atpic.coordinates.pack(lon,lat,wlen)
            print('XXX',((lon,lat),wlen,res),',')
            self.assertEqual(res,expect)

            res2=atpic.coordinates.unpack(res,wlen)
            print(((lon,lat),wlen,expect),res2)
            self.assertEqual(res2,(lon,lat))








    def NOtest_coord2(self):
        inputs=(
            (80,1),
            (80,2),
            (80,3),
            (80,4),
            (180,1),
            (179,1),
            )
        i=0
        for (coord,wlen) in inputs:
            i=i+1
            print('++++++++++++++++',i,'++++++++++++++++++')
            atpic.coordinates.get_one_interval(coord,wlen)


    def test_get_facets(self):
        inputs=(
            
            (20,30,45,50) ,
            (0,179,0,89) ,
            (0,180,0,90) ,
            )
        i=0
        for (xmin,ymin,xmax,ymax) in inputs:
            i=i+1
            print('++++++++++++++++',i,'++++++++++++++++++')

            atpic.coordinates.get_facets(xmin,ymin,xmax,ymax)


    def NOtest_idempotent(self):
        for wlen in range(1,20):
            for coord in range(-180,180,10):
                print('+++++++++++++++++++++++++++++++++')
                print('doing',coord)
                
                ((i,j),(xi,xj))=atpic.coordinates.get_one_interval(coord,wlen)
                (wlen2,(i2,j2),(xi2,xj2))=atpic.coordinates.identify_facet(xi,xj)
                self.assertEqual((wlen,(i,j),(xi,xj)),(wlen2,(i2,j2),(xi2,xj2)))

    def test_idempotent_lat(self):
        for wlen in range(1,20):
            for coord in range(-90,90,10):
                print('+++++++++++++++++++++++++++++++++')
                print('doing',coord)
                
                ((i,j),(xi,xj))=atpic.coordinates.get_one_interval(coord,wlen,maxcoord=90)
                (wlen2,(i2,j2),(xi2,xj2))=atpic.coordinates.identify_facet(xi,xj,maxcoord=90)
                self.assertEqual((wlen,(i,j),(xi,xj)),(wlen2,(i2,j2),(xi2,xj2)))



if __name__=="__main__":
    unittest.main()
