'''
Created on 25 de ago. de 2016

@author: pabli
'''

from django.db import models
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.SatelliteState import SatelliteState





class CommandType(models.Model):
    code           = models.CharField('Codigo del tipo de comando', max_length=24, help_text='Codigo del tipo de comando', unique=True)
    description    = models.CharField('Decripcion del tipo de comando', max_length=100, help_text='Decripcion del tipo de comando', unique=True)
    satellite      = models.ForeignKey(Satellite, related_name='commandsType')
    satelliteStates= models.ManyToManyField(SatelliteState, related_name='commandsType')
    active         = models.BooleanField(default=True)
    transactional  = models.BooleanField(default=False) 
    timeout        = models.IntegerField('Tiempo en segundos?', default=0, null=False) 
    notes          = models.TextField('Consecuencias, restricciones del comando', max_length=512, null=True)
    maxRetry       = models.IntegerField(default=2)
    
    def __str__(self):
        return self.code
    