'''
Created on Sep 27, 2016

@author: ubuntumate
'''
from django.db import models
from GroundSegment.models.Consts import Consts


class MessageTemplate(models.Model):
    name = models.CharField('Nombre de la plantilla', max_length=Consts.smallString, help_text='Nombre de la plantilla', unique=True, default="sin nombre")
    subject = models.CharField('Asunto del mensaje', max_length=Consts.smallString, help_text='Asunto del mensaje', unique=True, default="sin nombre")
    text = models.TextField(null=False, default="Sin mensaje")
    
    
    
    def __str__(self):
        return self.name