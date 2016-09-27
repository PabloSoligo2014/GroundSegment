'''
Created on 3 de set. de 2016

@author: Pablo Soligo
'''

from django.db import models
from GroundSegment.models.Satellite import Satellite


class TmlyVarType(models.Model):
    code           = models.CharField('Codigo del tipo de variable', max_length=24, help_text='Codigo del satelite, ejemplo FS2017', unique=True)
    description    = models.CharField('Decripcion del tipo de variable', max_length=100, help_text='Decripcion del satelite', unique=True)
    