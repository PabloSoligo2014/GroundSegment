'''
Created on 4 de set. de 2016

@author: Pablo Soligo
'''

from django.db import models




class AlarmState(models.Model):
    code            = models.CharField('Codigo del estado de la alarma', max_length=24, help_text='Codigo del estado de la alarma', unique=True)
    description     = models.CharField('Decripcion del estado de la alarma', max_length=100, help_text='Decripcion del estado de la alarma', unique=True)
 

    def __str__(self):
        return self.code