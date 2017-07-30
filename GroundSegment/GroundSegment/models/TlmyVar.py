'''
Created on Oct 27, 2016

@author: ubuntumate
'''

from django.db import models
from GroundSegment.models.TlmyVarType import TlmyVarType

from GroundSegment.models.Alarm.Alarm import Alarm
from django.utils.timezone import datetime, now, timedelta, utc
from Calibration.GenericCalibration import GCalibration

class TlmyVar(models.Model):
    code        = models.CharField('Codigo del tipo de variable', max_length=24, help_text='Codigo de la variable, se quita relacion con maestro', default="NoDef")
    rawValue    = models.IntegerField(default=0)
    
    calIValue   = models.IntegerField(default=0)
    calFValue   = models.FloatField(default=0.0)
    calSValue   = models.CharField('Valor como string de la variable de telemetria', default=None, max_length=24, help_text='Valor como string de la variable de telemetria')
    
    created     = models.DateTimeField(auto_now_add=True)
    #created     = models.DateTimeField()
    #Quito la relacion para que no me obligue a guardar el padre
    #para despues guardar al hijo
    tmlyVarType = models.ForeignKey(TlmyVarType, related_name="tmlyVars")
    
    
    def getValue(self):
        #Retorna el valor en funcion del tipo
        
        if self.tmlyVarType.varType==self.tmlyVarType.INTEGER:
            return self.calIValue
        elif self.tmlyVarType.varType==self.tmlyVarType.FLOAT:
            return self.calFValue
        else:
            return self.calSValue
         
    def setValue(self, raw, saveifchange=False):
        #Optimizacion importante, solo salvo si el valor cambio con el anterior
        #cosa que normalmente no pasa!!
        #Si el raw anterior es igual al actual me libero de todo.
        if raw!=self.tmlyVarType.lastRawValue:
            self.tmlyVarType.lastRawValue = raw
            if self.tmlyVarType.calibrationMethod: 
                if not self.tmlyVarType.calibrationLogic:
                    klass = globals()[self.tmlyVarType.calibrationMethod.aClass]
                    instance = klass()
                    methodToCall = getattr(instance, self.tmlyVarType.calibrationMethod.aMethod)
                    self.tmlyVarType.calibrationLogic = methodToCall
                else:
                    pass #Calibracion ya cargada   
                
                if self.tmlyVarType.varType==self.tmlyVarType.INTEGER:
                    self.tmlyVarType.lastCalIValue = self.tmlyVarType.calibrationLogic(self.tmlyVarType,  raw )
           
                elif self.tmlyVarType.varType==self.tmlyVarType.FLOAT:
                    self.tmlyVarType.lastCalFValue = self.tmlyVarType.calibrationLogic(self.tmlyVarType,  raw )
                else:
                    self.tmlyVarType.lastCalSValue = self.tmlyVarType.calibrationLogic(self.tmlyVarType,  raw )
            else:
                if self.tmlyVarType.varType==self.tmlyVarType.INTEGER:
                    self.tmlyVarType.lastCalIValue = raw
                elif self.tmlyVarType.varType==self.tmlyVarType.FLOAT:
                    self.tmlyVarType.lastCalFValue = raw
                else:
                    self.tmlyVarType.lastCalSValue = raw 
                
            """
            Si el tipo no es cadena llevo el dato a cadena
            """
            
            value = self.tmlyVarType.getValue()
            
            if self.tmlyVarType.varType!=self.tmlyVarType.STRING:
                if (value>=self.tmlyVarType.limitMaxValue and value<=self.tmlyVarType.limitMinValue):
                    raise Exception("Invalid value in var "+self.tmlyVarType.code)  
                
            if saveifchange:
                self.tmlyVarType.lastUpdate = datetime.now(utc)
                self.tmlyVarType.save()
        
            """    
            if (value>self.maxValue or value<self.minValue):
                #Verificar si requiere alarma y crearla
                if self.alarmType != None:
                    sat = self.tmlyVarType.satellite
                    alarm = Alarm.new(sat, self, datetime.utcnow() + timedelta(seconds=-1))
                    alarm.save()
            """    
            
        if self.tmlyVarType.varType==self.tmlyVarType.INTEGER:
            self.calIValue = self.tmlyVarType.lastCalIValue
            self.calSValue = str(self.calIValue)
        elif self.tmlyVarType.varType==self.tmlyVarType.FLOAT:
            self.calFValue = self.tmlyVarType.lastCalFValue
            self.calSValue = str(self.calFValue)
        else:
            self.calSValue = self.tmlyVarType.lastCalSValue
            
        
 
        
        
        #Historico siempre, aunque el valor sea el mismo.
        #value = self.tmlyVarType.getValue()
        
        """
        Haya cambiado o no genero el registro
        de que se recibio telemetria
        """

        return self.tmlyVarType.getValue()

        
    def oldSetValue(self, raw):
        
        #Primero transformo en un valor calibrado para su posterior analisis de limites
        
        self.calSValue = "-"
        if self.tmlyVarType.varType==self.tmlyVarType.INTEGER:
            self.calIValue = raw
        elif self.tmlyVarType.varType==self.tmlyVarType.FLOAT:
            self.calFValue = raw
        else:
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
            
        