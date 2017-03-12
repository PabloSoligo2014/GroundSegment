'''
Created on Mar 11, 2017

@author: ubuntumate
'''
import unittest
from GroundSegment.models.Tle import Tle
from GroundSegment.models.SatelliteState import SatelliteState
from GroundSegment.models.Satellite import Satellite
from django.utils import timezone
from datetime import timedelta
from _datetime import tzinfo
from django.utils.timezone import pytz


class testTle(unittest.TestCase):


    
    def test01Descarga(self):
        try:
            
            ss, created = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
            
            
            iss = Satellite.new("ISS", "Estacion espacial internacional", 25544, ss)
            iss.save()
            tle = iss.getLastTLE()
            
            epoch = tle.getEpoch()
            
            """
            La epoca del tle debe estar entre ayer y mañana
            """
            yesterday = (timezone.datetime.utcnow()-timedelta(days=1) ).replace(tzinfo=pytz.utc)
            tomorrow = (timezone.datetime.utcnow()+timedelta(days=1) ).replace(tzinfo=pytz.utc)
            
            self.assertTrue( ( epoch>=yesterday  ) and \
                             ( epoch<=tomorrow  ), \
                             "Last tle datetime is incorrect" \
                            )\
                              
            
            newtle = iss.getLastTLE()
            
            
            
            self.assertTrue(tle.getEpoch()==newtle.getEpoch(), "Two downloaded TLE at the same time")
            
            """
            Ahora el tle esta actualizado, no debe descargar nuevamente
            """
            
        
        except Exception as ex:
            self.fail("Error durante el test de descarga: "+str(ex))
            
            
        def test02EphemBody(self):
            iss = Satellite.objects.get(code="ISS")
            tle = iss.getLastTLE()
            eb = tle.getAsEphemBody()
            
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDescarga']
    unittest.main()