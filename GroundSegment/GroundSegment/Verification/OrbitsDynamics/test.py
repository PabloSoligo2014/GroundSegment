'''
Created on Apr 14, 2017

@author: ubuntumate
'''
import unittest
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.SatelliteState import SatelliteState


class Test(unittest.TestCase):


    def test01DownloadLastTle(self):
        
        
        
        ss, created = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
        
        
        sat, created = Satellite.objects.get_or_create(code="ISS", description="ISS", noradId=25544, state=ss)

        if created:
            pass
        
        self.assertEqual(Satellite.objects.count(), 1, "Error en la cantidad de satelites, el satelite no fue creado")
            
    def test02abc(self):
        
        sat = Satellite.objects.get(code="ISS")
        
        tle = sat.getLastTLE()
        print(tle.epoch, tle.getLine1())
        eb = tle.getAsEphemBody()
        
        
        
        

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test01DownloadLastTle']
    unittest.main()