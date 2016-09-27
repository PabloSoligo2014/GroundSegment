'''
Created on Aug 29, 2016

@author: ubuntumate
'''

from django.db import models

from GroundSegment.models.Tle import Tle
from GroundSegment.models.Satellite import Satellite

class Propagation(models.Model):
    created     = models.DateTimeField(auto_now_add=True)
    tle         = models.ForeignKey(Tle, related_name='propagations')

    satellite   = models.ForeignKey(Satellite, related_name='propagations')
    final       = models.BooleanField(default = False)