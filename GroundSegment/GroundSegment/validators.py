'''
Created on Mar 15, 2017

@author: ubuntumate
'''

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_lat(value):
    if value>90 or value<-90:
        raise ValidationError(
            _('La latitud es incorrecta debe estar entre -90 y 90'),
            params={'value': value},
        )