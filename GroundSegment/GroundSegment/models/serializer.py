'''
Created on Jan 31, 2017

@author: ubuntumate
'''
from GroundSegment.models.DCPData import DCPData
from rest_framework.serializers import ModelSerializer

class FileSerializer(ModelSerializer):
    class Meta:
        model = DCPData
        fields = ('dcp_plataform', 'Temperature')