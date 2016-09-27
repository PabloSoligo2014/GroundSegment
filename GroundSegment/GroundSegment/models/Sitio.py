'''
Created on Sep 5, 2016

@author: ubuntumate
'''
from django.db import models
#from GroundSegment.models.Satellite import Satellite
#from django.contrib.admin.utils import help_text_for_field

class Sitio(models.Model):
    name = models.CharField("Nombre del Sitio", max_length=24, unique=True)
    lat  = models.FloatField('Latitud', help_text='[Dato en Grados Decimales]', unique=True)
    lon = models.FloatField('Longitud', help_text='[Grados Decimales]', unique=True)
    h = models.FloatField('altura', help_text='[metros]', unique=True)

    def __str__(self):
        return self.name