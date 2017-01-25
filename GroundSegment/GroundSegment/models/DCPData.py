'''
Created on Jan 25, 2017

@author: ubuntumate
'''

from django.db import models
from django.utils.timezone import datetime, now, timedelta, utc
from GroundSegment.models.DCPPlatform import DCPPlatform

class DCPData(models.Model):
 #   sitio       = models.ForeignKey(Sitio,related_name='DCPplatforms')
    dcp_plataform    = models.ForeignKey(DCPPlatform, related_name='dcpdatas')
    dataTime         = models.DateTimeField(auto_now_add=True)
    receive_dataTime = models.DateTimeField(auto_now_add=True)
    snow             = models.FloatField(help_text='Nieve_colchon',default=0.0)
    Precipitation    = models.FloatField(help_text='Precipitacion_Totalizador',default=0.0)
    Temperature      = models.FloatField(help_text='Temperatura [C]',default=0.0)
    Humidity         = models.FloatField(help_text='Humedad [%]',default=0.0)
    Wind_dir         = models.FloatField(help_text='Direccion del Viento [grados]',default=0.0)
    Wind_speed       = models.FloatField(help_text='Velocidad del viento [KPH]',default=0.0)
    Bat_volts        = models.FloatField(help_text='Tension de Bateria [volts]',default=0.0)
    cm_data          = models.FloatField(help_text='cm ???????',default=0.0)
    
    def __str__(self):
        return str(self.Temperature) 
    
