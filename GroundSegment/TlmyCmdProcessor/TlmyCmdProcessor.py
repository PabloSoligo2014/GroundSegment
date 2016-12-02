'''
Created on 15 de nov. de 2016
@author: Pablo Soligo
'''

"""
Interface con UHF y futuro procesador de telemetria. Conecta con un servidor TCP/IP provisto por el fabricante de la 
antena. El servidor envia paquetes tcp/ip tan pronto como los tiene disponible. La comunicacion es bidireccional y acepta 
telecomandos, eso aun no esta implementado.

TESTING: Puede ser testeado perfectamente usando un servidor TCP/IP virtual del tipo packetsender 
"""
import socket
import time
import datetime
from django.conf import settings
import os
import sys


#ubuntumate@VBUbuntumate:~/Downloads/CheckoutBox/Software$ java -jar start.jar
#C:\Users\pabli\Documents\Programas\CheckoutBox\Software java -jar start.jar
#python Main.py CUBESAT o SIMULATION

"""
Ejemplo de ejecucion 
>python TlmyCmdProcessor.py "SIMULATION" "C:\\Users\\pabli\\git\\GroundSegment\\GroundSegment" "FS2017"
"""


if __name__ == '__main__':
   
    """
    Valores por default  de path del proyecto y marca para guardado 
    de telemetria cruda (Marcar si el origen de la telemetria es simulado o real)
    El path del proyecto es dependiente de la maquina y por eso se deja configurable, 
    es necesario para poder leer y escribir sobre las entidades
    """
    #proj_path = "/home/ubuntumate/git/GroundSegment/GroundSegment"
    proj_path = "C:\\Users\\pabli\\git\\GroundSegment\\GroundSegment"
    source = "SIMULATION"
    satellite = "FS2017"
    module = "TlmyCmdProcessor"
    

        
    
    if len(sys.argv)>1:
        source      = sys.argv[1]
        proj_path   = sys.argv[2]
        satellite   = sys.argv[3] 
    
    #https://www.stavros.io/posts/standalone-django-scripts-definitive-guide/
    
    
    # This is so Django knows where to find stuff.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroundSegment.settings")
    sys.path.append(proj_path)
    os.chdir(proj_path)
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    try:
        #Si me desconecto intento nuevamente conectarme despues de un sleep
        #y asi in eternum....
        
        print("Reading configuration..")
        from GroundSegment.models.Satellite import Satellite
        from GroundSegment.models.UHFRawData import UHFRawData
        from GroundSegment.models.Parameter import Parameter
        from GroundSegment.models.TlmyVarType import TlmyVarType
        from GroundSegment.models.Log import Log
        from GroundSegment.Utils.Utils import *
        
        
        
        """
        Cargo todos los parametros de configuracion del sistema
        """
        uhfServerIp             = loadOrCreateParam("UHF_SERVER_IP", "GroundStation", "127.0.0.1", "IP del servidor TCP de la antena UHF")
        uhfServerPort           = loadOrCreateParam("UHF_SERVER_PORT", "GroundStation", "3210", "Puerto del servidor TCP de la antena UHF")    
        BUFFER_SIZE             = loadOrCreateParam("UHF_BUFFER_SIZE", "GroundStation", "1024", "Tamanio del buffer del cliente TCP")
        DISCONNECTION_SLEEP     = loadOrCreateParam("UHF_DISCONNECTION_SLEEP", "GroundStation", "10", "Tiempo en que se duerme la aplicacion ante una desconexion a la espera de volver a intentar")
    
        Log.create("UHFInterface started", "The uhf interface module was started", module, Log.INFORMATION).save()

        print("Done..trying to connect ip ", uhfServerIp, " ,port", uhfServerPort)
        
        while True:
            print("Create o recreate socket...", str(datetime.datetime.utcnow()) )
            """
            Creo el socket -Cliente- que se conectara al software de la antena
            """            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                """
                Precargo todas los tipos variables de telemetria del satellite enviado como parametro, lo hago 
                aqui para hacerlo solo una vez, para mejorar el software se deberia pensar en una recarga cada intervalo
                de tiempo determinado para si cambian la configuracion tomar los cambios
                """
                telvars = TlmyVarType.objects.filter(satellite__code="FS2017")
                
                
                """
                Intento conectarme segun ip y puerto configurado 
                """
                s.connect( (uhfServerIp, int(uhfServerPort)) )
                try:
                    print("Successfully connection to..", uhfServerPort)
                    while True:
                        """
                        Me quedo esperando recibir informacion
                        """                        
                        chunk = s.recv(int(BUFFER_SIZE))
                        
                        """
                        Si la informacion no es una trama de bits completa la proceso
                        """
                        if chunk == b'':
                            raise RuntimeError("socket connection broken")
                        else:
                            """
                            Me guardo el crudo tal cual llego antes de procesarlo, la tabla donde se guarda es UHFRawData
                            """
                            print("Len-",len(chunk))
                            print("\nData Received("+str(datetime.datetime.utcnow())+")->", chunk)
                            data = UHFRawData()
                            data.source = source
                            data.data = chunk
                            data.save()
                                                        
                            """
                            Ahora proceso los datos en funcion de las variables de telemetria configuradas en el sistema. 
                            Las mismas ya tienen internamente sus funciones de calibracion segun configuracion
                            """
                            
                            """
                            Recorro todas los tipos de variable de telemetria, las busco en la posicion en la trama, 
                            y actualizo su valor, la clase TlmyVarType internamente se encarga de todo, la transformacion en variable
                            de ingenieria y la persistencia en tiempo real e historica
                            """
                            for tt in telvars:
                                """
                                code draft
                                val = chunk[tt.position]
                                tt.setValue(val)
                                
                                """
                                
                        ##f.close()
                finally:
                    s.close()
            
            except Exception as err:
                Log.create("ERROR UHFInterface", "Error/Exception "+str(err), module, Log.ERROR).save()
                #TODO, quitar print
                print(err)
                 
            except IOError as err2:
                Log.create("IOERROR UHFInterface", "Error/Exception "+str(err2), module, Log.ERROR).save()
                #TODO, quitar print
                print("Error..")
                
              
            print("Sleeping..")
            time.sleep(int(DISCONNECTION_SLEEP))
                    
    except ValueError as ve:
        Log.create("Failed connection..", "Error/Exception "+str(ve), module, Log.ERROR).save()
        print("Failed connection..")
        
    print("Finalized")
    
        
    

        