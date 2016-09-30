'''
Created on 16 de ago. de 2016

@author: pabli
'''

from django.contrib import admin
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Tle import Tle
from GroundSegment.models.Parameter import Parameter
from GroundSegment.models.CommandType import CommandType
from GroundSegment.models.CommandTypeParameter import CommandTypeParameter  
from GroundSegment.models.SatelliteState import SatelliteState
#from GroundSegment.models.Pasada import Pass
from GroundSegment.models.Alarm.AlarmType import AlarmType
from GroundSegment.models.Alarm.Alarm import Alarm
from GroundSegment.models.Alarm.Criticity import Criticity
from GroundSegment.models.Alarm.AlarmState import AlarmState
from GroundSegment.models.Pasada import Pasada
from GroundSegment.models.Sitio import Sitio

from GroundSegment.models.Notification.AlarmTypeNotificationType import AlarmTypeNotificationType
from GroundSegment.models.Notification.Contact import Contact
from GroundSegment.models.Notification.MessageTemplate import MessageTemplate
from GroundSegment.models.Notification.Notification import Notification
from GroundSegment.models.Notification.NotificationType import NotificationType

class SatelliteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Satellite, SatelliteAdmin)

class ParameterAdmin(admin.ModelAdmin):
    pass

admin.site.register(Parameter, ParameterAdmin)

class CommandTypeAdmin(admin.ModelAdmin):
    empty_value_display = ''
    fields = ('code', 'description', 'active', 'transactional', 'satellite', 'satelliteStates', 'timeout', 'notes')
    list_display = ('code', 'description', 'transactional', 'satellite', 'timeout', 'notes')
    #list_filter = (NameFilter,)
    search_fields = ['code']

admin.site.register(CommandType, CommandTypeAdmin)



class SatelliteStateAdmin(admin.ModelAdmin):
    pass

admin.site.register(SatelliteState, SatelliteStateAdmin)


class AlarmTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(AlarmType, AlarmTypeAdmin)


class AlarmAdmin(admin.ModelAdmin):
    pass

admin.site.register(Alarm, AlarmAdmin)


class CriticityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Criticity, CriticityAdmin)

class AlarmStateAdmin(admin.ModelAdmin):
    pass

admin.site.register(AlarmState, AlarmStateAdmin)


class PasadaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Pasada,PasadaAdmin)

class SitioAdmin(admin.ModelAdmin):
    pass
admin.site.register(Sitio,SitioAdmin)

class ContactAdmin(admin.ModelAdmin):
    fields = ('name', 'email',)
    list_display = ('name', 'email',)
admin.site.register(Contact ,ContactAdmin)

class AlarmTypeNotificationTypeAdmin(admin.ModelAdmin):
    
    fields = ('notificationType', 'alarmType', 'messageTemplate', 'contacts',)
    list_display = ('notificationType', 'alarmType', 'messageTemplate',)
admin.site.register(AlarmTypeNotificationType ,AlarmTypeNotificationTypeAdmin)



class MessageTemplateAdmin(admin.ModelAdmin):
    pass
admin.site.register(MessageTemplate ,MessageTemplateAdmin)

class NotificationTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(NotificationType ,NotificationTypeAdmin)

class NotificationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notification ,NotificationAdmin)
