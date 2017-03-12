'''
Created on Mar 11, 2017

@author: ubuntumate
'''
import unittest
from GroundSegment.models.Tle import Tle
from GroundSegment.models.SatelliteState import SatelliteState
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Sitio import Sitio
from django.utils import timezone
from datetime import timedelta
from _datetime import tzinfo
from django.utils.timezone import pytz
from GroundSegment.models.Country import Country
from GroundSegment.models.State import State


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
        self.assertIsNone(eb, "No es generado el objeto tle como body")
        
    def test03PassGeneration(self):
        
        
        country, created = Country.objects.get_or_create(code="ARG", name="Argentina", description="Argentina")
        state, created = State.objects.get_or_create(code="COR", name="Cordoba", description="Cordoba", country=country)
        
        st, created = Sitio.objects.get_or_create(name="ETC", lat=-31.524075, lon=-64.463522, h=730.0, maskElev=0, state)
        
        iss = Satellite.objects.get(code="ISS")
        tle = iss.getLastTLE()
        eb = tle.getAsEphemBody()
        
            
            
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDescarga']
    unittest.main()