'''
Created on 25 de nov. de 2016

@author: pabli
'''

import os, sys

sys.path.append('C:\\Users\\pabli\\git\\GroundSegment\\GroundSegment')
#sys.path.append('/home/ubuntumate/git/GroundSegment/GroundSegment/')

from GroundSegment.settings import BASE_DIR

import random as rn
from django.db.models.query import QuerySet
from django.db import transaction
import threading
import time
from django.db import connection
import psycopg2


n = 0
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

from GroundSegment.models.Calibration import Calibration
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.TlmyVarType import TlmyVarType
from GroundSegment.models.TmlyVar import TmlyVar
from GroundSegment.models.UHFRawData import UHFRawData
import struct



#1- 7 bytes - Destination Callsign
#2- 7 bytes - Source Callsign
#3- 2 bytes - Control Bytes
#4- Variable - Data bytes (Data sent by the OBC)
#5- 2 bytes - FCS (AX25 CRC)

if __name__ == '__main__':
    
    
    
    uhfs = UHFRawData.objects.filter(source="CUBESAT")
    
    for u in uhfs:
        str = ""
        
        print(u.getBlob())
        
        
        #print("str->", str)
        
            
    
    """
    struct.pack('>I', 5000) # works fine
    >>>'\x00\x00\x13\x88'
    
    struct.pack('>I', 50000) # has a weird "P" variable which the documentation says shouldn't occur with Endian order.
    >>>'\x00\x00\xc3P'
    
    >>> ord('P')
    80
    >>> hex(80)
    '0x50'
    >>> 
    
    bytearray((0x00, 0x00, 0xc3, 0x50)) == struct.pack(">I", 50000)
    struct.pack('>I', 50000).encode("hex") '0000c350'
    
    

    
    datatype1 = "98 82 84 40 40 40 00 88 8A AC 96 92 A8 00 03 F0 01 A7 00 B0 00 00 00 00 E7 00 EC 00 31 CC CC 39 02 98 01 BA 03 04 00 04 00 00 00 3D 00 DF 00 E7 01 00 00 00 00 00 00 00 00 7F 1F 62 00 13 00 13 00 13 00 13 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 05 AD 00 00 00 00 27 DF 0A BF 0A DF 0A 04 00 04 00 04 00 00 16 6B D3"
    datatype2 = "98 82 84 40 40 40 00 88 8A AC 96 92 A8 00 03 F0 04 14 01 24 01 00 00 02 97 01 B5 03 04 00 04 00 00 00 3F 00 E1 00 E7 01 FA 75"
    datatype3 = "E2 08 80 3C 38 98 E2 2A 16 14 F2 74 54 45 DA 66 6D 16 49 E6"
    
    splDt1 = datatype1.split(" ")
    splDt2 = datatype2.split(" ")
    #print(spl)
    
    framecommand=bytearray.fromhex(splDt1[16])
    print("Dt1", framecommand)
    
    framecommand=bytearray.fromhex(splDt2[16])
    print("Dt2", framecommand)
    
    print("4b", splDt1[17:17+4])
    
    str1 = ''.join(e for e in splDt1[17:17+4])
    framelength=bytearray.fromhex(str1)
    print("Framel, ", framelength)
    
    print("Frame length: ", struct.unpack('<I', framelength) )
    
    """
    
    
    

    #uhf = UHFRawData.objects.filter(source="CUBESAT")
    
    
        
    
    
    
    
    