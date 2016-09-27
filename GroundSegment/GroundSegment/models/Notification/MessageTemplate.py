'''
Created on Sep 27, 2016

@author: ubuntumate
'''
from django.db import models


class MessageTemplate(models.Model):
    text = models.TextField(null=False, default="Sin mensaje")
    
    
    def __str__(self):
        return self.text