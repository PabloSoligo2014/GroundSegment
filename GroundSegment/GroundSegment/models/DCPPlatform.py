'''
Created on Jan 25, 2017

@author: ubuntumate
'''


from django.db import models

class DCPPlatform(models.Model):
    code = models.CharField('Codigo de la Plataforma', max_length=24, help_text='Codigo de la Plataforma', unique=True)
    
    def __str__(self):
        return self.code