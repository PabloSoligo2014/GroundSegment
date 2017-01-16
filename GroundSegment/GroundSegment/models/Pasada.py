'''
Created on Sep 2, 2016

@author: ubuntumate
'''

from django.db import models
import ephem
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Tle import Tle
from GroundSegment.models.Sitio import Sitio

class Pasada(models.Model):
    satellite   = models.ForeignKey(Satellite, related_name='pasadas')
    tle         = models.ForeignKey(Tle, related_name='pasadas', null=True)
    sitio       = models.ForeignKey(Sitio,related_name='pasadas')
    startTime   = models.DateTimeField(auto_now_add=True)
    stopTime    = models.DateTimeField(auto_now_add=True)
    duration    = models.FloatField('Duracion', help_text='[minutos]', default=0.0)

    def __str__(self):
        return self.name
    
    
    
    