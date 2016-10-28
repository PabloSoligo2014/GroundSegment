'''
Created on 3 de set. de 2016

@author: Pablo Soligo
'''

from django.db import models
import sys
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Alarm.Alarm import Alarm



class TlmyVarType(models.Model):
    code           = models.CharField('Codigo del tipo de variable', max_length=24, help_text='Codigo del satelite, ejemplo FS2017', unique=True)
    description    = models.CharField('Decripcion del tipo de variable', max_length=100, help_text='Decripcion del satelite', unique=True)
    
    satellite      = models.ForeignKey(Satellite, related_name="tmlyVarType")
    
    limitMaxValue  = models.FloatField(default=sys.float_info.max)
    limitMinValue  = models.FloatField(default=sys.float_info.min)
    
    maxValue       = models.FloatField(default=0)
    minValue       = models.FloatField(default=0)
    
    alarmType = models.ForeignKey(Alarm, related_name="tmlyVarType", null=True) 
    
    
    