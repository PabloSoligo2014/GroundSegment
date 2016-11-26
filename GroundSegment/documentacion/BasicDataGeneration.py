
from GroundSegment.settings import BASE_DIR
import os, sys

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
            
    


from GroundSegment.models.Satellite import Satellite
from GroundSegment.models import Tle, SatelliteState
from GroundSegment.models.Alarm.Criticity import Criticity
from django.utils.timezone import datetime, now, timedelta, utc
from _datetime import datetime
from GroundSegment.models.Alarm.AlarmType import AlarmType
from GroundSegment.models.Alarm.Alarm import Alarm
from GroundSegment.models.Site import Site
from django.core.exceptions import ObjectDoesNotExist
from GroundSegment.models.Alarm.Criticity import Criticity


try:    
    ss = SatelliteState.objects.get(code="NOMINAL")
except ObjectDoesNotExist:
    ss = SatelliteState()
    ss.code = "NOMINAL"
    ss.description = "NOMINAL"
    ss.save()


try:
    sat2 = Satellite.objects.get(code="FS2017")
except ObjectDoesNotExist:
    sat2 = Satellite.new("FS2017", "FS2017", 25544)
    sat2.state = ss
    sat2.save()
    
cr = Criticity()
cr.code = "MEDIA"
cr.color = 0
cr.description = "MEDIA"
cr.save()


at = AlarmType()
at.code = "ST01"
at.description = "Sobre tension en bla bla"
at.criticity = cr
at.timeout = 60
at.save()
            
            
from GroundSegment.models.Satellite import Satellite
sat = Satellite.objects.all()[0]
from GroundSegment.models.Alarm.AlarmType import AlarmType
al = AlarmType.objects.all()[0]
from django.utils.timezone import datetime, now, timedelta, utc
from GroundSegment.models.Alarm.Alarm import Alarm
al = Alarm.new(sat, al, datetime.now(utc))


from GroundSegment.models.Notification.AlarmTypeNotificationType import AlarmTypeNotificationType
atnt = AlarmTypeNotificationType.objects.all()[0]
from GroundSegment.models.Notification.Notification import Notification
Notification.new(alarmTypeNotificationType=atnt)

from GroundSegment.models.Alarm.AlarmType import AlarmType
st01 = AlarmType.objects.get(code="ST01")
from GroundSegment.models.Alarm.Alarm import Alarm
from GroundSegment.models.Satellite import Satellite
sat = Satellite.objects.get(code="FS2017")
from django.utils.timezone import datetime, now, timedelta, utc

al = Alarm.new(sat, st01, datetime.now(utc))

from GroundSegment.models.SubSystem import SubSystem
sub=SubSystem()
sub.code = "AOCS"
sub.description = "Acttitude and orbit control system"
sub.save()


