'''
Created on Oct 27, 2016

@author: ubuntumate
'''

from django.db import models
from GroundSegment.models.TlmyVarType import TlmyVarType

from GroundSegment.models.Alarm.Alarm import Alarm
from django.utils.timezone import datetime, now, timedelta, utc

class TmlyVar(models.Model):
    
    rawValue    = models.IntegerField(default=0)
    
    calIValue   = models.IntegerField(default=0)
    calFValue   = models.FloatField(default=0.0)
    calSValue   = models.CharField('Valor como string de la variable de telemetria', default=None, max_length=24, help_text='Valor como string de la variable de telemetria')
    
    tmlyVarType = models.ForeignKey(TlmyVarType, related_name="tmlyVars")
    
    
    def getValue(self):
        #Retorna el valor en funcion del tipo
        
        if self.tmlyVarType.varType==self.tmlyVarType.INTEGER:
            return self.calIValue
        elif self.tmlyVarType.varType==self.tmlyVarType.FLOAT:
            return self.calFValue
        else:
            return self.calSValue
            
        
    def setValue(self, raw):
        
        #Primero transformo en un valor calibrado para su posterior analisis de limites
        self.calIValue = raw
        self.calFValue = raw
        self.calSValue = str(raw)
        """        
        value = self.getValue()
        
        
        if (value>self.tmlyVarType.maxValue or value<self.tmlyVarType.minValue):
            #Verificar si requiere alarma y crearla
            if self.tmlyVarType.alarmType != None:
                sat = self.tmlyVarType.satellite
                alarm = Alarm.new(sat, self.tmlyVarType, datetime.utcnow() + timedelta(seconds=-1))
                alarm.save()
        """ 
            
        