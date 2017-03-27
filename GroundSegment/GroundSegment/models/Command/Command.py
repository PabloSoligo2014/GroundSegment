'''
Created on Mar 24, 2017

@author: ubuntumate
'''
from django.db import models
from GroundSegment.models.Command.CommandType import CommandType
from GroundSegment.models.Satellite import Satellite

from django.utils.timezone import datetime, now, timedelta
import pytz
#from GroundSegment.models.Satellite import Satellite
#from GroundSegment.models.SatelliteState import SatelliteState

class Command(models.Model):
    
    
    COMMAND_STATE = (
        (0, 'Pending'),
        (1, 'Sent'),
        (2, 'Failed'),
        (3, 'Executed'),
        (4, 'Expirated'),
    )


    
    
    commandType = models.ForeignKey(CommandType, related_name="commands")
    created     = models.DateTimeField()
    sent        = models.DateTimeField(null=True)
    executed    = models.DateTimeField(null=True)
    state       = models.IntegerField(choices=COMMAND_STATE, default=0)
    retry       = models.IntegerField(default=0)
    """
    TODO: Meter los parametros del comando!!!
    """
    satellite   = models.ForeignKey(Satellite, related_name="commands")
    expiration  = models.DateTimeField()
    
    
    def setExpirated(self):
        self.state  = 4
        self.save()
    
    def setSent(self):
        if self.retry>=self.commandType.maxRetry:
            self.setFailed()
        else:
            if self.sent==None:
                self.sent   = datetime.utcnow().replace(tzinfo=pytz.UTC)
            self.state  = 1
            self.retry = self.retry + 1
            self.save()
            
    def setExecuted(self):
        self.executed = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.state = 3
        self.save()
        
    def setFailed(self):
        self.executed = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.state = 2
        self.save()
        
    
    
    def send(self):
        self.save()
        
    def getState(self):
        return self.COMMAND_STATE[self.state]
    
    
    
    def __str__(self):
        return "Cmd: "+str(self.pk)+" tipo: "+self.commandType.code

"""
Console test...
"""
    