'''
Created on Aug 14, 2017

@author: ubuntumate
'''
import unittest
from GroundSegment.models.SatelliteState import SatelliteState


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test01SatelliteState(self):
        print("test.....")
        st1 = SatelliteState()
        st1.code = "Nominal"
        st1.description = "Nominal"
        st1.save()
        
        st2 = SatelliteState()
        st2.code = "Emergencia"
        st2.description = "Emergencia"
        st2.save()
        
        self.assertEqual(SatelliteState.objects.count(), 2, "La cantidad de estados es incorrecta")
        
        self.assertEqual(SatelliteState.objects.filter(code="Nominal").count(), 1, "No se encontro el estado!")
        
        
        
        
        
    def test02Satellite(self):
        pass
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()