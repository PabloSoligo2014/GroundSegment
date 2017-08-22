'''
Created on Aug 16, 2017

@author: ubuntumate
'''

import os, sys




proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.Command.CommandType import CommandType
from GroundSegment.models.Command.Command import Command
from GroundSegment.models.Command.CommandParameter import CommandParameter
from GroundSegment.models.Command.CommandTypeParameter import CommandTypeParameter
from datetime import datetime, timedelta





if __name__ == '__main__':
    fs2017 = Satellite.objects.get(code="FS2017")
    ct = fs2017.getCommandType().get(code="beaconOBC")
    cmd = fs2017.newCommand(ct, datetime.utcnow()+timedelta(minutes=5))
    cmd.addParameters(5)
    
    print("Hola")
    