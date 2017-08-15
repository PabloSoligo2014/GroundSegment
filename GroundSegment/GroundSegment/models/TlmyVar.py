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
    tlmyVarType = models.ForeignKey(TlmyVarType, related_name="tlmyVars")
    
    
    def getValue(self):
        #Retorna el valor en funcion del tipo
        
        if self.tlmyVarType.varType==self.tlmyVarType.INTEGER:
            return self.calIValue
        elif self.tlmyVarType.varType==self.tlmyVarType.FLOAT:
            return self.calFValue
        else:
            return self.calSValue
         
    def setValue(self, raw, saveifchange=False):
        #Optimizacion importante, solo salvo si el valor cambio con el anterior
        #cosa que normalmente no pasa!!
        #Si el raw anterior es igual al actual me libero de todo.
        if raw!=self.tlmyVarType.lastRawValue:
            self.tlmyVarType.lastRawValue = raw
            if self.tlmyVarType.calibrationMethod: 
                if not self.tlmyVarType.calibrationLogic:
                    klass = globals()[self.tlmyVarType.calibrationMethod.aClass]
                    instance = klass()
                    methodToCall = getattr(instance, self.tlmyVarType.calibrationMethod.aMethod)
                    self.tlmyVarType.calibrationLogic = methodToCall
                else:
                    pass #Calibracion ya cargada   
                
                if self.tlmyVarType.varType==self.tlmyVarType.INTEGER:
                    self.tlmyVarType.lastCalIValue = self.tlmyVarType.calibrationLogic(self.tlmyVarType,  raw )
           
                elif self.tlmyVarType.varType==self.tlmyVarType.FLOAT:
                    self.tlmyVarType.lastCalFValue = self.tlmyVarType.calibrationLogic(self.tlmyVarType,  raw )
                else:
                    self.tlmyVarType.lastCalSValue = self.tlmyVarType.calibrationLogic(self.tlmyVarType,  raw )
            else:
                if self.tlmyVarType.varType==self.tlmyVarType.INTEGER:
                    self.tlmyVarType.lastCalIValue = raw
                elif self.tlmyVarType.varType==self.tlmyVarType.FLOAT:
                    self.tlmyVarType.lastCalFValue = raw
                else:
                    self.tlmyVarType.lastCalSValue = raw 
                
            """
            Si el tipo no es cadena llevo el dato a cadena
            """
            
            value = self.tlmyVarType.getValue()
            
            if self.tlmyVarType.varType!=self.tlmyVarType.STRING:
                if (value>=self.tlmyVarType.limitMaxValue and value<=self.tlmyVarType.limitMinValue):
                    raise Exception("Invalid value in var "+self.tlmyVarType.code)  
                
            if saveifchange:
                self.tlmyVarType.lastUpdate = datetime.now(utc)
                self.tlmyVarType.save()
        
            """    
            if (value>self.maxValue or value<self.minValue):
                #Verificar si requiere alarma y crearla
                if self.alarmType != None:
                    sat = self.tlmyVarType.satellite
                    alarm = Alarm.new(sat, self, datetime.utcnow() + timedelta(seconds=-1))
                    alarm.save()
            """    
            
        if self.tlmyVarType.varType==self.tlmyVarType.INTEGER:
            self.calIValue = self.tlmyVarType.lastCalIValue
            self.calSValue = str(self.calIValue)
        elif self.tlmyVarType.varType==self.tlmyVarType.FLOAT:
            self.calFValue = self.tlmyVarType.lastCalFValue
            self.calSValue = str(self.calFValue)
        else:
            self.calSValue = self.tlmyVarType.lastCalSValue
            
        
 
        
        
        #Historico siempre, aunque el valor sea el mismo.
        #value = self.tlmyVarType.getValue()
        
        """
        Haya cambiado o no genero el registro
        de que se recibio telemetria
        """

        return self.tlmyVarType.getValue()

        
    def oldSetValue(self, raw):
        
        #Primero transformo en un valor calibrado para su posterior analisis de limites
        
        self.calSValue = "-"
        if self.tlmyVarType.varType==self.tlmyVarType.INTEGER:
            self.calIValue = raw
        elif self.tlmyVarType.varType==self.tlmyVarType.FLOAT:
            self.calFValue = raw
        else:
            self.calSValue = str(raw)

        
        """        
        value = self.getValue()
        
        
        if (value>self.tlmyVarType.maxValue or value<self.tlmyVarType.minValue):
            #Verificar si requiere alarma y crearla
            if self.tlmyVarType.alarmType != None:
                sat = self.tlmyVarType.satellite
                alarm = Alarm.new(sat, self.tlmyVarType, datetime.utcnow() + timedelta(seconds=-1))
                alarm.save()
        """ 
            
        