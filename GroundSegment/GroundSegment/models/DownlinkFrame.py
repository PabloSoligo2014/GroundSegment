'''
Created on Jan 30, 2017

@author: ubuntumate
'''

from django.db import models
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.SatelliteState import SatelliteState
from django.db.models.deletion import CASCADE




class DownlinkFrame(models.Model):
    
    
    
    frameCommand   = models.IntegerField('frame Command', help_text='frame Command')
    frameLength    = models.IntegerField('Dimension del frame', help_text='Dimension del frame')
    dataRate       = models.IntegerField('Tasa de transferencia', help_text='Tasa de transferencia')
    modulationName = models.CharField('Nombre de la modulacion', max_length=24, help_text='Nombre de la modulacion' )
    rssi           = models.FloatField(help_text='RSSI')
    frequency      = models.FloatField(help_text='Frecuencia')
    packetLength   = models.IntegerField('Dimension del paquete', help_text='Dimension del paquete')
    satellite      = models.ForeignKey(Satellite, on_delete=CASCADE, related_name="downloadlinkFrames")
    
    
    
    def __str__(self):
        return str(self.frameCommand)
    