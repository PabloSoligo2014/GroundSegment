'''
Created on Sep 27, 2016

@author: ubuntumate
'''

from django.db import models
from GroundSegment.models.Alarm.Alarm import Alarm

class Notification(models.Model):
    """
    Notifacion efectiva enviada o por enviar. Generada a partir de la configuracion del sistema
    
    Objetivo
    =========
        Repositorio para las notificaciones generadas y enviadas.
    
     
    Implementacion
    =========
        Se utiliza una unica entidad, las notificaciones se marcan como envidas cuando pueden ser despachadas o se
        indican la cantidad de intentos y se marcan como fallidas
    """  
    
    alarm   = models.ForeignKey(Alarm, related_name="notifications", on_delete=models.PROTECT, null=True)
    """
    Alarma asociada a la notificacion, puede no existir si la notificacion fuera generada por otro evento\n
    distinto a la generacion de la alarma
    """
    text = models.TextField(null=False, default="Sin mensaje")
    """
    Texto de la notificacion
    """
    
    
    sended  = models.BooleanField(default=False)
    ntry    = models.IntegerField(default=0)
    
    def __str__(self):
        return "Notificacion: " + str(self.pk)
    
    
    
    #CASCADE[source]
    #PROTECT[source]
    #SET_NULL[source]
    #SET_DEFAULT[source]