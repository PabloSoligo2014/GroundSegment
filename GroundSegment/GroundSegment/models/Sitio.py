'''
Created on Sep 5, 2016

@author: ubuntumate
'''
from django.db import models
import ephem
from GroundSegment.models.Satellite import Satellite
from datetime import datetime
from GroundSegment.Utils.UtilsFunctions import *
from GroundSegment.models.State import State
#from django.contrib.admin.utils import help_text_for_field

class Sitio(models.Model):
    name     = models.CharField("Nombre del Sitio", max_length=24, unique=True)
    lat      = models.FloatField('Latitud', help_text='[Dato en Grados Decimales]')
    lon      = models.FloatField('Longitud', help_text='[Grados Decimales]')
    h        = models.FloatField('Altura', help_text='[metros]')
    maskElev = models.FloatField('Mascara de Elevacion', help_text='[grados]', default=0.0)
    
    state    = models.ForeignKey(State,related_name='sitios', null=True)

    def __str__(self):
        return self.name
    
    def getPass(self,satcode,idate):
        from GroundSegment.models.Pasada import Pasada
        '''
        Sitio
        '''
        print("---------------PROXIMA PASADA----------------")
        
#        site=Sitio.objects.get(name='ETC')
        
        obs            = ephem.Observer()
        obs.lon        = self.lon
        obs.lat        = self.lat
        obs.elevation  = self.h
        obs.horizon    = self.maskElev
        obs.date       = ephem.Date(idate)
       
        '''
        Satelite
        '''
        
        satelite = Satellite.objects.get(code=satcode)
        print("NORAD ID = %s" % (satelite.noradId))
        
#         tle0 = satelite.getLastTLE()
#         print(tle0.getLine1())
               
        line1 = satelite.code
        line2="1 99937U          19245.00000000 -.00000688  00000-0 -74340-4 0 00007"
        line3 = "2 99937 097.7872 318.3601 0010609 271.6129 088.3852 14.88384890000013"
        sat0 = ephem.readtle(line1, line2, line3)
        info = obs.next_pass(sat0)
#         FS2017.compute(site)
#         print(FS2017.alt,FS2017.eclipsed)
        print("Rise time: %s Set Time: %s Duration [m]: %f" % (info[0], info[4],(info[4]-info[0])*1440))
        
        """
        Registro de la pasada
        """
        pasada0             = Pasada()
        pasada0.satellite   = satelite
        pasada0.sitio       = self
        pasada0.startTime   = datetime_from_time(info[0])
        pasada0.stopTime    = datetime_from_time(info[4])
        pasada0.duration    = (info[4]-info[0])*1440
        
        pasada0.save()
        
        
        return None
    
    def getPasses(self, satellite, afrom, ato):
        """
        Obtiene la tabla de pasadas completa para un rango, las tablas se generar en bloques
        de un dia si ya fue creada y con el ultimo TLE disponible
        retorna el resultado pero no recalcula si ya fue calculado antes
        """
        #TODO Seguir aca con la tabla de pasadas por dia!
        tle = satellite.getLastTLE()
        tle.epoch