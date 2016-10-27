'''
Created on Oct 27, 2016

@author: ubuntumate
'''

from django.db import models
from GroundSegment.models.TlmyVarType import TmlyVarType

from GroundSegment.models.Alarm.Alarm import Alarm
from django.utils.timezone import datetime, now, timedelta, utc

class TmlyVar(models.Model):
    value = models.FloatField()
    tmlyVarType = models.ForeignKey(TmlyVarType, related_name="tmlyVars")
    
    def setValue(self, value):
        if (value>self.tmlyVarType.limitMaxValue or value<self.tmlyVarType.limitMinValue):
            raise Exception("Invalid value in var "+self.tmlyVarType.code)  
        
        self.value = value
        if (value>self.tmlyVarType.maxValue or value<self.tmlyVarType.minValue):
            #Verificar si requiere alarma y crearla
            if self.tmlyVarType.alarmType != None:
                sat = self.tmlyVarType.satellite
                alarm = Alarm.new(sat, self.tmlyVarType, datetime.utcnow() + timedelta(seconds=-1))
                alarm.save()
            
            
        