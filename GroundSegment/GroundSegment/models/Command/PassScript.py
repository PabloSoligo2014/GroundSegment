'''
Created on Mar 24, 2017

@author: ubuntumate
'''

from django.db import models
from django.utils.timezone import datetime, now, timedelta, utc
from GroundSegment.models.DCPPlatform import DCPPlatform
from django.contrib.auth.models import User
from GroundSegment.models.Pasada import Pasada
from GroundSegment.models.Satellite import Satellite


class PassScript(models.Model):
    
    created         = models.DateTimeField(auto_now_add=True)
    author          = models.ForeignKey(User, related_name='passScripts')  
    satellite       = models.ForeignKey(Satellite, related_name='passScripts')
    script          = models.TextField(default="Poner inclusion de django aca", help_text="Codifique el scripts", max_length=5120)
    apass           = models.ForeignKey(Pasada, related_name="passScripts", null=True)
    applied         = models.BooleanField(default=False)
    
    
    
    
    def __str__(self):
        return str(self.Temp_max) 
    

