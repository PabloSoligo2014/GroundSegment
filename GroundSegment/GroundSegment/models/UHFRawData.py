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
from struct import *




class UHFRawData(models.Model):
    created     = models.DateTimeField(auto_now_add=True)
    data        = models.BinaryField()
    source      = models.CharField('Origen del dato, tipicamente cubesat/simulacion', max_length=24, help_text='Origen del dato, tipicamente cubesat/simulacion', default='simulation')
    
    
    def getBlob(self):
        return unpack_from('c', self.data, offset=8)
    
"""  



def getBlobVectorSize(blobData):
    blobSize = unpack_from('!I',blobData, offset=4)
    return blobSize[0]

def readBlob(blobData):
    blobEncoding = unpack_from('!I',blobData, offset=0)
    formatStr = "!"

    if (blobEncoding[0] == 23):       #encoding vector<double> 

        vectorSize = getBlobVectorSize(blobData)       
        for x in range(0, vectorSize):
            formatStr += "d"

    else:
        raise ValueError("Unexpected blob encoding: %d" % blobEncoding[0])

    return getBlobVectorValues(blobData,formatStr)
    
"""

        