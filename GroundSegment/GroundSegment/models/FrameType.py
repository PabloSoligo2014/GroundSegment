'''
Created on Jan 30, 2017

@author: ubuntumate
'''

from django.db import models

class FrameType(models.Model):
    aid           = models.IntegerField('id del tipo de paquete', help_text='id del tipo de paquete', unique=True)
    description  = models.CharField('Decripcion del tipo de paquete', max_length=100, help_text='Decripcion del tipo de paquete')
    
    
    def __str__(self):
        return str(self.id)+", "+self.description
    