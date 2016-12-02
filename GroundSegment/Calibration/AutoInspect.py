'''
Created on 28 de nov. de 2016

@author: pabli
'''
"""
Ahora por reflexion genero en la base todos los metodos
"""

import os, sys, inspect
sys.path.append('/home/ubuntumate/git/GroundSegment/GroundSegment/')

from GroundSegment.settings import BASE_DIR
import GroundSegment



ROOT_DIR = BASE_DIR
proj_path = ROOT_DIR
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
    
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
                
           

import imp

#MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')
MODULE_EXTENSIONS = ('.py')
package_name = "Calibration"
file, pathname, description = imp.find_module(package_name)
if file:
    raise ImportError('Not a package: %r', package_name)
# Use a set because some may be both source and compiled.
files = set([os.path.splitext(module)[0] for module in os.listdir(pathname) if module.endswith(MODULE_EXTENSIONS)])

import Calibration

for f in files:
    ##print(f)
    ##print("----------")
    m = __import__(f)
    clsmembers = inspect.getmembers(m, inspect.isclass)
    
    for c in clsmembers:
        aclass = c[1]
        if issubclass(aclass, Calibration.BaseCalibration.BaseCalibration) and aclass!=Calibration.BaseCalibration.BaseCalibration:
            print(aclass)
            methods = inspect.getmembers(aclass, inspect.isfunction)
            
            for me in methods:
                amethod = me[1]
                l = GroundSegment.models.Calibration.objects.filter(aClass=aclass.__name__).filter(aMethod=amethod.__name__)
                if len(l)==0:
                    calmethod           = GroundSegment.models.Calibration()
                    calmethod.aClass    = aclass.__name__
                    calmethod.aMethod   = amethod.__name__
                    calmethod.subsystem = GroundSegment.models.SubSystem.objects.order_by('?').first()
                    calmethod.save()
                    print("Valor guardado")
    
    