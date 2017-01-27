'''
Created on Jan 25, 2017

@author: ubuntumate
'''


from django.db import models

from django.utils.timezone import datetime, now, timedelta, utc


class DCPPlatform(models.Model):
    code = models.CharField('Codigo de la Plataforma', max_length=24, help_text='Codigo de la Plataforma', unique=True)
    
    def __str__(self):
        return self.code
    
    def setData(self, datetime, snow, precipitation, temperature, humidity, windDir, windSpeed, batVolt, cmData):
        #TODO, poner datos en tiempo real en esta entidad y utilizar setData para guardar historicos
        #y setear tiempo real, por ahora solo tiempo real
        from GroundSegment.models.DCPData import DCPData
        dspData = DCPData()
        dspData.dcp_plataform   = self
        dspData.dataTime        = datetime
        dspData.receive_dataTime= utc
        dspData.snow            = snow
        dspData.Precipitation   = precipitation
        dspData.Temperature     = temperature
        dspData.Humidity        = humidity
        dspData.Wind_dir        = windDir
        dspData.Wind_speed      = windSpeed
        dspData.Bat_volts       = batVolt
        dspData.cm_data         = cmData
        dspData.save()
        
        return dspData
        
        