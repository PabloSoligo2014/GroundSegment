'''
Created on Mar 24, 2017

@author: ubuntumate
'''
from django.db import models
from GroundSegment.models.Command.CommandType import CommandType
from GroundSegment.models.Satellite import Satellite
#from GroundSegment.models.Satellite import Satellite
#from GroundSegment.models.SatelliteState import SatelliteState

class Command(models.Model):
    commandType = models.ForeignKey(CommandType, related_name="commands")
    created     = models.DateTimeField()
    sent        = models.DateTimeField(null=True)
    executed    = models.DateTimeField(null=True)
    retry       = models.IntegerField(default=0)
    """
    TODO: Meter los parametros del comando!!!
    """
    satellite   = models.ForeignKey(Satellite, related_name="commands")
    expiration  = models.DateTimeField()
    
    
    def send(self):
        self.save()
    
    
    
    def __str__(self):
        return "Tipo de comando: "+self.commandType.code

"""
Console test...


"""
    