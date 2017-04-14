'''
Created on Apr 14, 2017

@author: ubuntumate
'''
import ephem
import unittest
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.SatelliteState import SatelliteState


class Test(unittest.TestCase):


    def test01DownloadLastTle(self):
        
        
        
        ss, created = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
        
        
        sat, created = Satellite.objects.get_or_create(code="SACD", description="SACD", noradId=37673, state=ss)

        if created:
            pass
        
        self.assertEqual(Satellite.objects.count(), 1, "Error en la cantidad de satelites")
            
    def test02abc(self):
        """
        Propagaciones en Lat y Long.
        http://stackoverflow.com/questions/15937413/python-satellite-tracking-with-spg4-pyephem-positions-not-matching
        """
        
        sat = Satellite.objects.get(code="SACD")       
        tle = sat.getLastTLE()
        print (tle.getLine1())
        print (tle.getLine2())
        eb = tle.getAsEphemBody()
        d = ephem.Date('2017/4/14 12:00')
    
        for k in range(10):
            eb.compute(d)
            print (d,eb.sublat,eb.sublong)
            d=ephem.date(d + ephem.minute)

#         

#         print (date,eb.sublat, eb.sublong)
        
        
        
        
        

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test01DownloadLastTle']
    unittest.main()