'''
Created on Mar 26, 2017

@author: ubuntumate
'''
import unittest
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.SatelliteState import SatelliteState
from GroundSegment.models.Command.Command import Command
from GroundSegment.models.Command.CommandType import CommandType
from GroundSegment.models.Command.CommandTypeParameter import CommandTypeParameter
from GroundSegment.models.Command.PassScript import PassScript

from django.utils.timezone import datetime, now, timedelta

class Test(unittest.TestCase):


    def setUp(self):
        ss, created = SatelliteState.objects.get_or_create(code="NOMINAL", description="NOMINAL")
        sat = Satellite.new("FS2017", "FS2017", 2017, ss)
        sat.save()
        
        ct = CommandType.create("GT", "Get Telemetry", sat, ss, False, 60, "Sin notas", 3)
        ct.save()


    def tearDown(self):
        pass


    def testCreateCommand(self):
        
        sat = Satellite.objects.get(code="FS2017")
        ct  = CommandType.objects.get(code="GT")
        
        cmd = ct.newCommand(sat, now()+timedelta(minutes=60))
        
        cmd.send()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateCommand']
    unittest.main()