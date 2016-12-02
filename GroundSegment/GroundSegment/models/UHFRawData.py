'''
Created on Nov 16, 2016

@author: ubuntumate
'''

from datetime import *
from requests import *
from sgp4.earth_gravity import wgs72
from django.db import models
from django.utils.timezone import datetime, now, timedelta, utc


from sgp4.io import twoline2rv
from GroundSegment.models.SatelliteState import SatelliteState
from GroundSegment.models.Parameter import Parameter
from django.db.models.query import QuerySet





class UHFRawData(models.Model):
    created     = models.DateTimeField(auto_now_add=True)
    data        = models.BinaryField()
    source      = models.CharField('Origen del dato, tipicamente cubesat/simulacion', max_length=24, help_text='Origen del dato, tipicamente cubesat/simulacion', default='simulation')
    
    


        