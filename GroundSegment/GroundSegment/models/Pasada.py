'''
Created on Sep 2, 2016

@author: ubuntumate
'''
from datetime import datetime, timedelta
from django.db import models
import ephem
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Tle import Tle
from GroundSegment.models.Sitio import Sitio
from GroundSegment.models.PassGeneration import PassGeneration
from django.db.models.deletion import CASCADE

class Pasada(models.Model):
    """
    TODO: Mucha informacion redundante, hablar con Ceci para sacarla sino el diseno queda mal
    """
    
    satellite       = models.ForeignKey(Satellite, related_name='pasadas')
    tle             = models.ForeignKey(Tle, related_name='pasadas', null=True)
    sitio           = models.ForeignKey(Sitio,related_name='pasadas')
    startTime       = models.DateTimeField()
    stopTime        = models.DateTimeField()
    duration        = models.FloatField('Duracion', help_text='[minutos]', default=0.0)
    passGeneration  = models.ForeignKey(PassGeneration, on_delete=CASCADE, related_name="passes")
    
    

    def getDuration(self):
        return (self.stopTime-self.startTime).total_seconds()
    
    def getDurationStr(self):
        """
        pasar la duracion de la pasada a un string que indique min:sec
        """
        intervalo=(self.stopTime-self.startTime).total_seconds()
        minutos = int(intervalo//60)
        segundos= int((intervalo % 60))

        return '%s:%s' % (str(minutos).zfill(2),str(segundos).zfill(2))#(self.stopTime-self.startTime)
        
    
    def save(self, *args, **kwargs):
        self.duration = self.getDuration()
        super(Pasada, self).save(*args, **kwargs)

    def __str__(self):
        return self.satellite.code+", "+self.sitio.name+", "+str(self.startTime)+"-"+str(self.stopTime)
    
    
    
    