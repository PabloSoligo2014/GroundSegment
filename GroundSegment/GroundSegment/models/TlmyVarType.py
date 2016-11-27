'''
Created on 3 de set. de 2016

@author: Pablo Soligo
'''

from django.db import models
import sys
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Alarm.Alarm import Alarm
from GroundSegment.models.Calibration import Calibration
from django.utils.timezone import datetime, now, timedelta, utc
from test.test_logging import DerivedLogRecord
from pip._vendor.distlib.util import DIRECT_REF



class TlmyVarType(models.Model):
    
    INTEGER = 0
    FLOAT   = 1
    STRING  = 2
    
    DIRECT  = 0
    DERIVED = 1
    
    VARTYPE = (
        (INTEGER, 'Integer'),
        (FLOAT, 'Float'),
        (STRING, 'String'),
    )
    
    VARSUBTYPE= (
        (DIRECT, 'Direct'),
        (DERIVED, 'Derived'),
        
    )
    #, db_index=True
    code           = models.CharField('Codigo del tipo de variable', max_length=24, help_text='Codigo del satelite, ejemplo FS2017', unique=True)
    description    = models.CharField('Decripcion del tipo de variable', max_length=100, help_text='Decripcion del satelite', unique=True)
    
    satellite      = models.ForeignKey(Satellite, related_name="tmlyVarType")
    
    limitMaxValue  = models.FloatField(default=sys.float_info.max)
    limitMinValue  = models.FloatField(default=sys.float_info.min)
    
    maxValue       = models.FloatField(default=0)
    minValue       = models.FloatField(default=0)
    
    lastRawValue   =  models.IntegerField(default=0)
    lastCalIValue  =  models.IntegerField(default=0)
    lastCalFValue  =  models.FloatField(default=0.0)
    lastCalSValue  =  models.CharField('Valor como string de la variable de telemetria', default=None, max_length=24, help_text='Valor como string de la variable de telemetria', blank=True, null=True)
         
    
    varType        = models.IntegerField("Tipo de dato, 0=Integer, 1=Float, 2=String", default=0, choices=VARTYPE)    
    varSubType     = models.IntegerField("Indica si es directa o derivada 0=Directa, 1=Derivada", default=0, choices=VARSUBTYPE)
    alarmType      = models.ForeignKey(Alarm, related_name="tmlyVarType", blank=True, null=True) 
    calibrationMethod = models.ForeignKey(Calibration, related_name="tlmyVarTypes", blank=True, null=True)
    
    def getValue(self):
        #Retorna el valor en funcion del tipo
        
        if self.varType==self.INTEGER:
            return self.lastCalIValue
        elif self.varType==self.FLOAT:
            return self.lastCalFValue
        else:
            return self.lastCalSValue
    
    def setValue(self, raw):
        from GroundSegment.models.TmlyVar import TmlyVar
        #Primero transformo en un valor calibrado para su posterior analisis de limites
        self.lastCalIValue = raw
        self.lastCalFValue = raw
        self.lastCalSValue = str(raw)
        
        #Cuando seteo una variable automaticamente creo el historico
        
               
        value = self.getValue()
        
        tvar = TmlyVar()
        tvar.tmlyVarType = self
        tvar.setValue(value)
        
        #tvar.save()
        
        if (value>=self.limitMaxValue and value<=self.limitMinValue):
            raise Exception("Invalid value in var "+self.code)  
        """    
        if (value>self.maxValue or value<self.minValue):
            #Verificar si requiere alarma y crearla
            if self.alarmType != None:
                sat = self.tmlyVarType.satellite
                alarm = Alarm.new(sat, self, datetime.utcnow() + timedelta(seconds=-1))
                alarm.save()
        """    
        
    