'''
Created on Aug 24, 2016

@author: Pablo Soligo
'''

from django.db import models
from GroundSegment.models.Satellite import Satellite

#     created     = models.DateTimeField(editable=False)
#     modified    = models.DateTimeField()
# 
#     def save(self, *args, **kwargs):
#         #On save, update timestamps
#         if not self.id:
#             self.created = timezone.now()
#         self.modified = timezone.now()
#         return super(User, self).save(*args, **kwargs)
    

class Tle(models.Model):
    """
    Clase/Entidad TLE.
    Almacena la informacion de los TLE incluyendo su fecha de descarga y la epoca de TLE 
    """
    
    tleDateTime = models.DateTimeField(auto_now_add=True)
    """
    Fecha generacion del TLE, si no fuera seteada se utilizara la fecha hora actual
    """
    downloaded = models.DateTimeField(auto_now_add=True)
    """
    Fecha de descarga del TLE
    """
    
    lines = models.TextField(max_length=124, )
    """
    Lineas del TLE
    """
    
    satellite = models.ForeignKey(Satellite, related_name='tles')
    #latest() method
    """
    Satelite asociado al TLE
    """
    
    def getLine1(self):
        """
        Retorma la primera linea del TLE en formato texto plano
        @rtype:   string
        @return:  primera linea del TLE en texto plano.
        """

        
        return self.lines.split("\n")[0]
    
    
    def getLine2(self):
        """
        Retorma la segunda linea del TLE en formato texto plano
        @rtype:   string
        @return:  segunda linea del TLE en texto plano.
        """
        return self.lines.split("\n")[1]

        
    class Meta:
        get_latest_by = "tleDateTime"  
        
    