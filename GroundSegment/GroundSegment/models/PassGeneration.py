'''
Created on Mar 12, 2017

@author: ubuntumate
'''
from django.db import models
import ephem
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Tle import Tle
from GroundSegment.models.Sitio import Sitio
from datetime import timedelta
from django.utils.timezone import pytz


"""
Es el maestro (Master/Detail) de la generacion de pasadas, se guarda el dia el TLE con el que
fue generada y queda relacionado con las pasadas, antes de regenerar 
pasadas para un dia determinado se revisa si ya no fue generado y con que tle.
"""
class PassGeneration(models.Model):
    created     = models.DateTimeField(auto_now_add=True)
    tle         = models.ForeignKey(Tle, related_name='passGenerations')
    satellite   = models.ForeignKey(Satellite, related_name='passGenerations')
    sitio       = models.ForeignKey(Sitio,related_name='passGenerations')
    day         = models.DateField("Fecha que se toma en consideracion")
    
    @classmethod
    def create(cls, day, tle, satellite, sitio):
        result = cls()
        
        result.day = day
        result.tle = tle
        result.satellite = satellite
        result.sitio = sitio
        result.save()
        
        """
        Ahora genero los hijos, tengo toda la informacion para hacerlo
        """
        from GroundSegment.models.Pasada import Pasada
        observer    = result.sitio.getAsEphemObserver()
        sat         = result.tle.getAsEphemBody()
        
        pivotdate = day
        untildate = pivotdate + timedelta(days=1)
            
        while pivotdate<=untildate:
            observer.date = ephem.Date( pivotdate )         
                
            try:
                rise_time, rise_azimuth, maximum_altitude_time, maximum_altitude, set_time, set_azimuth = observer.next_pass(sat)
                #print(s.code, rise_time, rise_azimuth, maximum_altitude_time, maximum_altitude, set_time, set_azimuth)
                #node1, node2, afrom, ato, open, constellation):
                
                if rise_time.datetime()>set_time.datetime():
                    #Si esto sucede lo mas probable es que el satelite ya este visible...por tanto la rise time es ahora y la set time es la 
                    #rise time que viene como parametro
                    rt = pivotdate
                else:
                    rt = rise_time.datetime()
                    st = set_time.datetime()
                    
                #Deberia pasar los rise time/set time a utc
                
                rt = rt.replace(tzinfo=pytz.UTC)
                st = st.replace(tzinfo=pytz.UTC)
                
                """
                Creo la pasada, mucha informacion redundante que debe ser quitada
                """
                p = Pasada()
                
                """
                TODO: Informacion redundante QUITAR!
                """
                p.satellite = result.satellite
                p.tle = result.tle
                p.sitio = result.sitio
                p.passGeneration = result
                p.startTime = rt
                p.endTime   = st
                p.save()
              
                        
                observer.date = ephem.date( st )
                pivotdate = st.replace(tzinfo=pytz.UTC)
            except Exception as ValueError:
                #ValueError('that satellite seems to stay always below your horizon',)
                pivotdate = pivotdate+timedelta(minutes=1)
                print(ValueError)

        
        return result
        