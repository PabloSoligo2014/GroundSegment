'''
Created on 25 de nov. de 2016

@author: pabli
'''

import os, sys

from GroundSegment.settings import BASE_DIR

import random as rn
from django.db.models.query import QuerySet



if __name__ == '__main__':
    
  
    #ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    #proj_path = "/home/ubuntumate/git/GroundSegment/GroundSegment"
    
    ROOT_DIR = BASE_DIR
    #proj_path = "C:\\Users\\pabli\\git\\GroundSegment\\GroundSegment"
    proj_path = ROOT_DIR
     #https://www.stavros.io/posts/standalone-django-scripts-definitive-guide/
    
    # This is so Django knows where to find stuff.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
    sys.path.append(proj_path)
    
    
    # This is so my local_settings.py gets loaded.
    os.chdir(proj_path)
    
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
            
    
    """
    Primero que nada creamos 100.000 variables de telemetria si aun no existen
    
    """
    from GroundSegment.models.Satellite import Satellite
    from GroundSegment.models.TlmyVarType import TlmyVarType
    
    cant = TlmyVarType.objects.all().count()
    createcount = 100000-cant
    sat = Satellite.objects.get(code="FS2017")
    
    

    afrom = cant
    tlmVarTypeList = []
    ra = rn.Random()
    
    
    for i in range(afrom, createcount):
        
        tm = TlmyVarType()
        tm.satellite = sat
        tm.code = "VS"+str(i)
        tm.description = "Variable simulada n "+str(i)
        tm.limitMaxValue = ra.randrange(50.0, 100.0)
        tm.limitMinValue = ra.randrange(0.0, 49.0)
        
        tm.maxValue = tm.limitMaxValue
        tm.minValue = tm.limitMinValue
        
        tm.setValue(ra.randrange(tm.minValue, tm.maxValue))
        
        tm.varType = tm.FLOAT
        tm.varSubType = tm.DERIVED
        if i<10000:
            tm.varSubType = tm.DIRECT
        
        tlmVarTypeList.append(tm)
        #tm.save()
    
    import time  
    
    if len(tlmVarTypeList)>0:
        
        print("100.000 tipos de variables generadas, listo para guardar")
        t0 = time.time()
        TlmyVarType.objects.bulk_create(tlmVarTypeList)
        t1 = time.time()
        print("Variables almacenadas, tiempo de guardado...", t1-t0)
        
    
    #Supongo que por frame de telemetria me pueden llegar 500 variables,
    #selecciono 500 al azar
    print("Generando elementos de simulacion")
    allTlmyVar = TlmyVarType.objects.filter(satellite=sat).filter(varSubType=TlmyVarType.DIRECT)
    
    tlmySimulator = {}
    for x in range(500):
        tm = allTlmyVar.order_by('?').first()
        tlmySimulator[tm.pk] = tm.getValue()
        
    print("Elementos de simulacion generados, se simula..")
    
    tstart = time.time()
    #dirtyObj = []
    for k, v in tlmySimulator.items():
        tel = allTlmyVar.get(pk=k)        
        tel.setValue(v)
        
    allTlmyVar.update()
    tend = time.time()
    
    print("Simulacion para ",len(tlmySimulator), " telemetrias se realizo en ", tend-tstart)
        
        
    tstart = time.time()
    dAllTlmyVar = {}
    for t in allTlmyVar:
        dAllTlmyVar[t.pk] = t
    
    for k, v in tlmySimulator.items():
        tel = dAllTlmyVar[k]       
        tel.setValue(v)
        
    allTlmyVar.update()
    tend = time.time()
    
    print("Igual simulacion con diccionario demora ", tend-tstart)
  
    """
    
    from Calibration.GenericCalibration import *

    raw = 2
    
    obj = getattr(sys.modules[__name__], "GenericCalibration")
    
    cal = getattr(obj, "duplicateAndSum")(obj, raw)
    
    print("Valor calibrado: ", cal)
    """
    
    