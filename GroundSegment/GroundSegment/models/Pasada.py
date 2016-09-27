'''
Created on Sep 2, 2016

@author: ubuntumate
'''

from django.db import models
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Sitio import Sitio

class Pasada(models.Model):
    name = models.CharField(max_length=128, unique=True)
    satellite   = models.ForeignKey(Satellite, related_name='pasadas')
    sitio = models.ForeignKey(Sitio,related_name='pasadas')
    startTime = models.DateTimeField(auto_now_add=True)
    stopTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
    