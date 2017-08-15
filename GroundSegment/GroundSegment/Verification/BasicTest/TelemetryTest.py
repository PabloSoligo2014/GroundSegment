'''
Created on Aug 15, 2017

@author: ubuntumate
'''
import unittest

from GroundSegment.models.SatelliteState import SatelliteState
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.FrameType import FrameType
from GroundSegment.models.UnitOfMeasurement import UnitOfMeasurement
from GroundSegment.models.TlmyVarType import TlmyVarType
from GroundSegment.models.TlmyVar import TlmyVar

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test01SatelliteState(self):
        print("test..2...")
        st1 = SatelliteState()
        st1.code = "Nominal"
        st1.description = "Nominal"
        st1.save()

    def test02Satellite(self):
        
        try:
            st = SatelliteState.objects.first()
            sat = Satellite.new("FS2017", "Satelite Formador 2017", 98745, st)
            sat.save()
        except:
            pass


    def test03FrameType(self):
        frame_type = FrameType()
        frame_type.aid = 1
        frame_type.description = "AllTelemetry"
        frame_type.save()


    def test04UnitOfMeasurement(self):
        unit_M = UnitOfMeasurement()
        unit_M.code = "C"
        unit_M.description = "Grados Celcius"
        unit_M.save()


    def test04Telemetry(self):
        tlmy_varType = TlmyVarType()
        tlmy_varType.code = "PATemp"
        tlmy_varType.description = "PATemp fullname"
        sat = Satellite.objects.first()
        tlmy_varType.satellite = sat 
        tlmy_varType.limitMaxValue = 999.999
        tlmy_varType.limitMinValue = -999.999
        tlmy_varType.maxValue = 999.999
        tlmy_varType.minValue = -999.999
        tlmy_varType.varType = 1
        tlmy_varType.frameType = FrameType.objects.first()
        tlmy_varType.save()



    def test05Telemetry(self):
        print("test05Telemetry")
        tlmy_varType = TlmyVarType.objects.get(code="PATemp")
        
        tlmv = TlmyVar()
        
        tlmv.code = tlmy_varType.code
        tlmv.tlmyVarType = tlmy_varType
        
        tlmv.setValue(25)
        tlmv.save()
        
        
        self.assertEqual(tlmy_varType.getValue(), TlmyVar.objects.filter(code="PATemp").order_by('pk').last().getValue(), "El el ultimo valor cargado no coincide con el de tiempo real")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()