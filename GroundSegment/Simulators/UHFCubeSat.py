'''
Created on 22 de dic. de 2016

@author: pabli
'''

import socket
import sys
import time
import struct
import datetime
from _datetime import timedelta
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")

from GroundSegment.settings import BASE_DIR


n = 0
ROOT_DIR = BASE_DIR
#proj_path = "C:\\Users\\pabli\\git\\GroundSegment\\GroundSegment"
proj_path = ROOT_DIR
 #https://www.stavros.io/posts/standalone-django-scripts-definitive-guide/
sys.path.append(proj_path)
os.chdir(proj_path)
# This is so Django knows where to find stuff.


# This is so my local_settings.py gets loaded.


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from GroundSegment.models.Calibration import Calibration
from GroundSegment.models.Satellite import Satellite
from GroundSegment.models.TlmyVarType import TlmyVarType
from GroundSegment.models.TmlyVar import TmlyVar
from GroundSegment.models.UHFRawData import UHFRawData



if __name__ == '__main__':
    
    BUFFER_SIZE = 2000
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('10.77.171.180', 3210)
    sock.bind(server_address)
    
    # Listen for incoming connections
    #Listen: El server se pone a escuchar conexiones de clientes en el puerto configurado (1), por ahora solo aceptamos una conexion
    sock.listen(1)
    
    
    #minutos = input("Ingrese cantidad de minutos para la prueba...")
    #frecuencia = input("Ingrese la frecuencia de la prueba...")
    
    # Wait for a connection
    print('waiting for a connection')
    #sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    
    while True:
        try:
            
            connection, client_address = sock.accept()
            
            print('Cliente conectado...')
            
            tiempoactual = datetime.datetime.utcnow()
            
            
            
            uhfs = UHFRawData.objects.filter(id__gte=1002, id__lte=1490)
            
            
            i = 0
            while True:
                print('connection from', client_address)
        
                #binaryClientData = connection.recv(BUFFER_SIZE)
                
                my_bytes = uhfs[i].getBlob()
                i = i + 1
                if i==uhfs.count():
                    i=0
                     
                connection.send (my_bytes)
                
                time.sleep(1)
        except Exception as err:
            print("Error: {0}".format(err))
        
        
        print('Reconexion post exception, esperando 10 segundos')
        time.sleep(3)
        print('Reconectando...')
        
    """
    try:
        
        # Receive the data in small chunks and retransmit it
        print('Hora de inicio de prueba:', tiempoactual)
        
        while tiempoactual + datetime.timedelta(minutes = int(minutos))>datetime.datetime.utcnow():
            
            
            #binaryClientData = connection.recv(BUFFER_SIZE)
            
            #if binaryClientData:
            #clientData = struct.unpack('4s', binaryClientData)
            #rint("Client Data, " , clientData)
                
                
                
            i =0
            while i < len(uhfs) and (tiempoactual + datetime.timedelta(minutes = int(minutos))>datetime.datetime.utcnow()):


                #pk = "hola que tal"+"\r"
                #pk = "hola que tal"
                #pk = struct.pack('4s', b'\x01\x00\x19\x59')
            
                #print('Enviando paquete')
                my_bytes = uhfs[i].getBlob()
                connection.send (my_bytes)
                #connection.send(linea_n[i][30:-1].encode(encoding='utf_8', errors='strict'))
                print('Paquete enviado')
                
                i = i + 1
                #connection.close()
                if i == len(uhfs) - 1:
                    i =0
                    
                    
                time.sleep(float(frecuencia))
                
                    
    finally:
        # Clean up the connection
        print('Hora de fin de prueba:', datetime.datetime.utcnow())
        
        connection.close()
        
    print('Finalizado')

    """