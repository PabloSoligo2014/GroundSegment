'''
Created on 25 de ago. de 2016

@author: pablosoligo
'''

from django.db import models


class CommandTypeParameter(models.Model):
    code           = models.CharField('Codigo del parametro', max_length=24, help_text='Codigo del parametro', default="NoDet")
    description    = models.CharField('Decripcion del parametro', max_length=100, help_text='Decripcion del satelite', default="NoDet")
    
    def __str__(self):
        return self.code
    