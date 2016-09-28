'''
Created on Sep 27, 2016

@author: ubuntumate
'''

from django.db import models
from GroundSegment.models.Alarm.Alarm import Alarm
from GroundSegment.models import Consts
from GroundSegment.models.Notification.Contact import Contact
from GroundSegment.models.Notification.NotificationType import NotificationType
from django.template.defaultfilters import default
from GroundSegment.models.Notification.AlarmTypeNotificationType import AlarmTypeNotificationType

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
    
    
    """
    Alarma asociada a la notificacion, puede no existir si la notificacion fuera generada por otro evento\n
    distinto a la generacion de la alarma
    """
    subject = models.CharField('Asunto de la notificacion', max_length=Consts.Consts.mediumString , help_text='Asunto de la notificacion', default="subject default")
    text = models.TextField(null=False, default="Sin mensaje")
    """
    Texto de la notificacion
    """
    contacts = models.ManyToManyField(Contact, related_name="notifications", limit_choices_to=100)
    
    alarmTypeNotificationType = models.ForeignKey(AlarmTypeNotificationType, related_name="notifications", on_delete=models.PROTECT, null=True)
    
    sended  = models.BooleanField(default=False)
    ntry    = models.IntegerField(default=0)
    
    @classmethod
    def new(cls, **kwargs):
        result = cls()
        """
        text = kwargs['text']
        subject = kwargs['subject']
        """
        
        #Por ahora solo acepto notificaciones con alarmas
        alarmTypeNotificationType = kwargs['alarmTypeNotificationType']
        
        
        result.alarmTypeNotificationType = alarmTypeNotificationType
        result.text = alarmTypeNotificationType.messageTemplate.text
        result.subject = alarmTypeNotificationType.messageTemplate.subject
        result.ntry = 0
        result.sended = False
        result.save()
        
        cnts = result.alarmTypeNotificationType.contacts.all()
        
        
        recipients = list( cnts.values_list('email', flat=True) )
            
        
        from GroundSegment.Utils.EMailThread import EmailThread
        EmailThread(result.subject, result.text, recipients).start()
                
        return result
    
    def __str__(self):
        return "Notificacion: " + str(self.pk)
    
    
    
    #CASCADE[source]
    #PROTECT[source]
    #SET_NULL[source]
    #SET_DEFAULT[source]