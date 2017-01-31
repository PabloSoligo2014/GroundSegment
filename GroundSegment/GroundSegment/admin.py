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
from GroundSegment.models.TlmyVarType import TlmyVarType
from GroundSegment.models.TmlyVar import TmlyVar

from GroundSegment.models.Calibration import Calibration
from GroundSegment.models.SubSystem import SubSystem
from GroundSegment.models.Log import Log
from GroundSegment.models.Coefficient import Coefficient

from GroundSegment.models.DCPPlatform import DCPPlatform
from GroundSegment.models.DCPData import DCPData



class SatelliteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Satellite, SatelliteAdmin)

class ParameterAdmin(admin.ModelAdmin):
    search_fields = ['module']
    list_display = ('module', 'key', 'value', 'description')

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


class CoefficientInline(admin.TabularInline):
    model = Coefficient

    

class TmlyVarTypeAdmin(admin.ModelAdmin):
    #fields = ()
    search_fields = ['code']
    list_display = ('code', 'description', 'satellite', 'lastCalFValue', 'lastUpdate', 'varType')
    
    inlines = [
        CoefficientInline,
    ]
    
admin.site.register(TlmyVarType ,TmlyVarTypeAdmin)

class TmlyVarAdmin(admin.ModelAdmin):
    pass
admin.site.register(TmlyVar ,TmlyVarAdmin)


class CalibrationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Calibration ,CalibrationAdmin)



class SubSystemAdmin(admin.ModelAdmin):
    pass
admin.site.register(SubSystem ,SubSystemAdmin)


class LogAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'module', 'logType')
    search_fields = ['module', 'logType']
    list_filter = ['module', 'logType']

    def get_queryset(self, request):
    #def queryset(self, request):
        qs = super(LogAdmin, self).get_queryset(request)
        tmp = qs.all().order_by("-id")
        return tmp
    
admin.site.register(Log ,LogAdmin)

class DCPPlatformAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(DCPPlatform ,DCPPlatformAdmin)

class DCPDataAdmin(admin.ModelAdmin):
    list_display = ('dcp_plataform', 'dataTime', 'snow', 'Precipitation', 'Temperature', 'Humidity', 'Wind_dir', 'Wind_speed', 'Bat_volts', 'cm_data' )
    readonly_fields=('dcp_plataform', 'dataTime', 'snow', 'Precipitation', 'Temperature', 'Humidity', 'Wind_dir', 'Wind_speed', 'Bat_volts', 'cm_data' )
admin.site.register(DCPData ,DCPDataAdmin)


from GroundSegment.models.FrameType import FrameType
class FrameTypeAdmin(admin.ModelAdmin):
    list_display = ( 'aid', 'description')
    
admin.site.register(FrameType ,FrameTypeAdmin)


from GroundSegment.models.UnitOfMeasurement import UnitOfMeasurement
class UnitOfMeasurementAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(UnitOfMeasurement ,UnitOfMeasurementAdmin)


