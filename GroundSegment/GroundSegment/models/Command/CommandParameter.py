'''
Created on Aug 16, 2017

@author: ubuntumate
'''
from django.db import models
from GroundSegment.models.Command.Command import Command


class CommandParameter(models.Model):
    
    command     = models.ForeignKey(Command,related_name="parameters")
    value       = models.CharField(max_length=5, default="")
    
    
    
        