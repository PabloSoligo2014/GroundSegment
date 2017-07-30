'''
Created on 28 de nov. de 2016

@author: pabli
'''
#from apport.hookutils import files_in_package
import Calibration
"""
Ahora por reflexion genero en la base todos los metodos
"""

import os, sys, inspect

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(proj_path)

#from GroundSegment.settings import BASE_DIR
import GroundSegment


def AutoInspect():
    #proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    
    proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(proj_path)
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
    os.chdir(proj_path)
    
        
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
                    
               
    
    import imp, importlib
    
    print("Insertando en la base de datos funciones de calibracion")
    #MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')
    MODULE_EXTENSIONS = ('.py')
    package_name = "Calibration"
    file, pathname, description = imp.find_module(package_name)
    if file:
        raise ImportError('Not a package: %r', package_name)
    # Use a set because some may be both source and compiled.
    files = set([os.path.splitext(module)[0] for module in os.listdir(pathname) if module.endswith(MODULE_EXTENSIONS)])
    
    
    import Calibration
    for md in sys.modules:
        print(md)
    
    for f in files:
        if f!="__init__" and f!="AutoInspect":
            md = "Calibration."+f
            clsmembers = inspect.getmembers(sys.modules[md], inspect.isclass)
            for clname, cldata in clsmembers:
                #print(clname)
                methods = inspect.getmembers(cldata, inspect.isfunction)
                for mtdName, amethod in methods:
                    l = GroundSegment.models.Calibration.objects.filter(aClass=clname).filter(aMethod=mtdName)
                    if len(l)==0:
                        calmethod           = GroundSegment.models.Calibration()
                        calmethod.aClass    = clname
                        calmethod.aMethod   = mtdName
                        calmethod.subsystem = GroundSegment.models.SubSystem.objects.order_by('?').first()
                        calmethod.save()
                        print("Valor guardado")
  
if __name__ == '__main__':
    AutoInspect()                    
    