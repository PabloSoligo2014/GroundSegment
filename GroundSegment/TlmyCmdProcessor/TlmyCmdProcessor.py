"""
@package docstring
Created on 15 de nov. de 2016
@author: Pablo Soligo

Interface con UHF y futuro procesador de telemetria. Conecta con un servidor TCP/IP provisto por el fabricante de la 
antena. El servidor envia paquetes tcp/ip tan pronto como los tiene disponible. La comunicacion es bidireccional y acepta 
telecomandos, eso aun no esta implementado.

TESTING: Puede ser testeado perfectamente usando un servidor TCP/IP de test del tipo packetsender 
    ->https://packetsender.com/
"""
import socket
import time
import datetime
from django.conf import settings
import os
import sys

from django.utils import timezone
from _struct import unpack



#ubuntumate@VBUbuntumate:~/Downloads/CheckoutBox/Software$ java -jar start.jar
#C:\Users\pabli\Documents\Programas\CheckoutBox\Software java -jar start.jar
#python Main.py CUBESAT o SIMULATION

"""
Ejemplo de ejecucion 
>python TlmyCmdProcessor.py "SIMULATION" "FS2017" 

Deprecated: Ya no es necesario indicar el path, lo toma del directorio de ejecucion del fuente "C:\\Users\\pabli\\git\\GroundSegment\\GroundSegment"
>python3.4 TlmyCmdProcessor.py "SIMULATION" "FS2017" 

Deprecated: Ya no es necesario indicar el path, lo toma del directorio de ejecucion del fuente "/home/ubuntumate/git/GroundSegment/GroundSegment" 
"""


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def is_set(x, n):
    return x & 2**n != 0 




"""Servicio, aplicacion encargada de decodificar, trasnformar y persistir la telemetria del satelite y de codificar y transmitir los 
telecomandos.
@param source Indica si la ejecucion es para servir a una simulacion o datos reales. Los paquetes persistidos quedan con esta cadena como marca
para uso futuro y especialmente para poder distinguir datos simulados de datos reales.
@param satellite Codigo de satelite con el que se esta comunicando. El satelite tiene que estar dado de alta en el catalogo. La trama de telemetria sera
decodificada en funcion de la configuracion de variables de telemetria del satelite indicado como parametro
"""
if __name__ == '__main__':
    
    PosFrameCommand         = 0
    LenFrameCommand         = 1
    
    PosFrameLen             = PosFrameCommand+LenFrameCommand
    LenFrameLen             = 4
    
    PosDataRate             = PosFrameLen+LenFrameLen
    LenDataRate             = 4
    
    PosModuluationNameLen   = PosDataRate+LenDataRate 
    LenModuluationNameLen   = 1
    
    PosModulationName       = PosModuluationNameLen+LenModuluationNameLen
    LenModulationName       = 0
    
    PosRSSI                 = PosModulationName+LenModulationName 
    LenRSSI                 = 8
    
    PosFrequency            = PosRSSI+LenRSSI
    LenFrequency            = 8
    
    PosPktLen               = PosFrequency+LenFrequency
    LenPktLen               = 2


    
    """Funcion principal del eervicio, aplicacion encargada de decodificar, trasnformar y persistir la telemetria del satelite y de codificar y transmitir los 
    telecomandos.
    @param source Indica si la ejecucion es para servir a una simulacion o datos reales. Los paquetes persistidos quedan con esta cadena como marca
    para uso futuro y especialmente para poder distinguir datos simulados de datos reales.
    @param satellite Codigo de satelite con el que se esta comunicando. El satelite tiene que estar dado de alta en el catalogo. La trama de telemetria sera
    decodificada en funcion de la configuracion de variables de telemetria del satelite indicado como parametro
    """
    
    
    
    """
    Valores por default para guardado 
    de telemetria cruda (Marcar si el origen de la telemetria es simulado o real)
    """
    
    """Obtiene el path del proyecto segun carpeta de ejecucion"""
    proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source = "SIMULATION"
    satellite = "FS2017"
    module = "TlmyCmdProcessor"
    

        
    
    if len(sys.argv)>1:
        source      = sys.argv[1]
        satellite   = sys.argv[2] 
    
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
        from GroundSegment.models.Watchdog import Watchdog
        from GroundSegment.Utils.Utils import *
        from GroundSegment.models.DownlinkFrame import DownlinkFrame 
        from GroundSegment.Managers.CommandManager import CommandManager
        
        
        """
        Si el watchdog no fue creado aun en ejecuciones anteriores lo creo ahora
        """
        
        wd, created = Watchdog.objects.get_or_create(
                                        code='TlmyCmdProcessor',
                                        description='Watchdog del procesador de telemetria y telecomandos',
                                        module="TlmyCmdProcessor",
                                        tolerance=10,
                                    )   
        
        
        
       
        """
        Log guardar en el registro de log los sucesos que se consideren relevante para futura autoria o debug
        """
        Log.create("TlmyCmdProcessor started", "The uhf interface module was started", module, Log.INFORMATION).save()

        sat     = Satellite.objects.get(code=satellite)
        cmdmgr  = CommandManager(sat)
        
        """
        Bucle infinito, el software debe funcionar 7x24, si el software de la antena no estuviera 
        funcionando simplemente se duerme un tiempo parametrizable y vuelve a intentar la conexion
        hasta que este disponible. Dado que no es posible instalarlo como servicio, el watchdog se 
        realizar manualmente.
        """
        
        
            
        while True:
            """
            Limite de conexiones fallidas antes de recargar configuracion...
            
            """
            """
            Cargo todos los parametros de configuracion del sistema
            """
            uhfServerIp             = loadOrCreateParam("UHF_SERVER_IP", "GroundStation", "127.0.0.1", "IP del servidor TCP de la antena UHF")
            uhfServerPort           = loadOrCreateParam("UHF_SERVER_PORT", "GroundStation", "3210", "Puerto del servidor TCP de la antena UHF")    
            BUFFER_SIZE             = loadOrCreateParam("UHF_BUFFER_SIZE", "GroundStation", "1024", "Tamanio del buffer del cliente TCP")
            DISCONNECTION_SLEEP     = loadOrCreateParam("UHF_DISCONNECTION_SLEEP", "GroundStation", "10", "Tiempo en que se duerme la aplicacion ante una desconexion a la espera de volver a intentar")
            cls()
            print("Done..trying to connect ip ", uhfServerIp, " ,port", uhfServerPort)
            unconnectionLimit       = 0
            i = 0
            while unconnectionLimit<10:
                cls()
                print("Create o recreate socket...", str(datetime.datetime.utcnow()) )
                """
                Creo el socket -Cliente- que se conectara al software de la antena
                """            
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    """
                    Precargo todas los tipos variables de telemetria del satelite enviado argumento, lo hago 
                    aqui para hacerlo solo una vez, para mejorar el software se deberia pensar en una recarga cada intervalo
                    de tiempo determinado por si cambian la configuracion tomar los cambios
                    """
                    
                    #Log.create("LoadTlmy", "Load telemetry var types, count: "+str(len(telvars)), module, Log.INFORMATION).save()
    
                    
                    
                    """
                    Intento conectarme segun ip y puerto configurado, si la configuracion 
                    estuviera mal o no estuviera el servidor levantado el componente
                    de socket informa mediante exception, la misma es trapeada para volver
                    a intentar ciclicamente (Informe de error mediante)
                    """
                    s.connect( (uhfServerIp, int(uhfServerPort)) )
                    try:
                        print("Successfully connection to..", uhfServerPort)
                        while True:
                            
                            
                            
                            try:
                                """
                                Establezco un timeout para la bajada, con o sin bajada los comandos deben ser enviados
                                """
                                s.settimeout(5.0)
                                
                                """
                                Me quedo esperando recibir informacion del socket (IPC)
                                """                        
                                chunk = s.recv(int(BUFFER_SIZE))
                                
                                unconnectionLimit = 0
                                
                                """
                                Buena o mala la telemetria fue recibida, reseteo el watchdog
                                """
                                wd.reset()
                                
                                """
                                Si recibo telemetria, defenitivamente estoy en contacto
                                """
                                sat.setInContact(True)
                                
                                """
                                Si la informacion es una trama de bits completa la proceso
                                """
                                if chunk == b'':
                                    raise RuntimeError("socket connection broken")
                                else:
                                    """
                                    Me guardo el crudo tal cual llego antes de procesarlo, la tabla donde se guarda es UHFRawData
                                    """
                                    
                                    print("\nData Received("+str(timezone.datetime.utcnow() )+"), Tamano: ", len(chunk), "\nData->", chunk)
                                    
                                    data = UHFRawData()
                                    data.source = source
                                    data.data = chunk
                                    data.processed = False
                                    data.save()
                                    
                                    framecommand = unpack("<B",chunk[PosFrameCommand:PosFrameCommand+LenFrameCommand])[0] 
                                    frameLength  = unpack("<I",chunk[PosFrameLen:PosFrameLen+LenFrameLen])
                                    datarate     = unpack("<I",chunk[PosDataRate:PosDataRate+LenDataRate])
                                    modulationnamelen = (unpack("<B",chunk[PosModuluationNameLen:PosModuluationNameLen+LenModuluationNameLen]))[0]
                                    modulationname    = chunk[PosModulationName:PosModulationName+modulationnamelen] 
                                    PosRSSI           = PosModulationName+modulationnamelen 
                                    rssi              = unpack("<d", chunk[PosRSSI:PosRSSI+LenRSSI])
                                    PosFrequency        = PosRSSI+LenRSSI
                                    freq                = unpack("<d", chunk[PosFrequency:PosFrequency+LenFrequency])
                                    PosPktLen           = PosFrequency+LenFrequency
                                    pktLen             = unpack("<H",  chunk[PosPktLen:PosPktLen+LenPktLen])
                                    PosUtcTime = PosPktLen+pktLen[0]
                                    LenUtcTime = 4
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    PosPayload = PosPktLen+int(LenPktLen)
                                    ax25 = chunk[PosPayload:PosPayload+pktLen[0]]
                                    
                                    
                                    destination  = ax25[0:7]
                                    asource      = ax25[7:7+7]
                                    control      = ax25[7+7:7+7+1]
                                    protocol     = ax25[7+7+1:7+7+1+1]
                                    
                            
                                         
                                    vardataoffset = 7+7+1+1
                                    payload = ax25[ vardataoffset: ]
                                    
                                    pn = unpack("<H",  payload[1:3])
                                    print("packet number:", pn)
                                    
                                    frameTypeId = payload[0]
                                    
                                    #print(framecommand, ", ", frameLength, ", ", datarate, ", ", modulationname, "rssi", rssi, "Freq ", freq, "PktLen", pktLen)
                                    
                                    dl = DownlinkFrame()
                                    
                                    dl.frameCommand     = framecommand
                                    dl.frameLength      = frameLength[0]
                                    dl.dataRate         = datarate[0]
                                    dl.modulationName   = str(modulationname)
                                    dl.rssi             = rssi[0]
                                    dl.frequency        = freq[0]
                                    dl.packetLength     = pktLen[0]
                                    dl.satellite        = sat
                                    dl.ax25Destination  = "Pending"#destination.decode("utf-8") 
                                    dl.ax25Source       = "Pending"#asource.decode("utf-8") 
                                    dl.ax25Protocol     = "Pending"#protocol.decode("utf-8") 
                                    dl.ax25Control      = "Pending"#control.decode("utf-8") 
                                    dl.packetNumber     = pn[0]
                                    dl.frameTypeId      = frameTypeId 
                                                                
                                    
                                    
                                    dl.save()
                                    
                                    
                                    
                                     
                                    #frameTypeId = unpack("<B",payload[0])
                                    
                                    telvars = TlmyVarType.objects.filter(satellite__code=satellite).filter(frameType__aid=frameTypeId)
                                    
                                    for tt in telvars:
                                        
                                        #TODO
                                        #code draft
                                        
                                        if tt.bitsLen >= 8:
                                            bitLen_div =tt.bitsLen // 8
                                            if bitLen_div == 1:
                                                raw = unpack("<B",  payload[tt.position:tt.position+bitLen_div])[0]
                                            else:
                                                raw = unpack("<H",  payload[tt.position:tt.position+bitLen_div])[0]
                                        else:
                                            raw = is_set(payload[tt.position], tt.bitsLen)                                         
                                                 
                                        
                                        
                                        tv = tt.setValue(raw, True)
                                        tv.save()
                                    
                                    print("\nData processed("+str(timezone.datetime.utcnow() )+")")
                                    data.processed = True
                                    data.save()
                                    
                                              
                                    #dl.processed = True                   
                                    """
                                    Ahora proceso los datos en funcion de las variables de telemetria configuradas en el sistema. 
                                    Las mismas ya tienen internamente sus funciones de calibracion segun configuracion
                                    """
                                    
                                    """
                                    Recorro todas los tipos de variable de telemetria, las busco en la posicion en la trama, 
                                    y actualizo su valor, la clase TlmyVarType internamente se encarga de todo, la transformacion en variable
                                    de ingenieria y la persistencia en tiempo real e historica
                                    """
                                    """
                                    
                                    """
                                    """
                                    <sequence_number position="1" type="short" xmlns="" name="packetNumber"/>
                                    <number position="3" type="int" xmlns="" name="OBCUpTime"/>
                                    <number position="7" type="char" xmlns="" name="commandCounter"/>
                                    """
    #                                 packetNumber    = chunk[1-2] "pack"
    #                                 OBCUpTime       = chunk[1,2,3,4]
    #                                 commandCounter  = chunk[7]
                                                         
                                ##f.close()
                            except socket.timeout:
                                #Error de timeout de sockets, si el satelite esta en linea 
                                print("Socket timeout")
                                
                            """
                            Si el satelite esta en linea debo mandar comandos pendientes
                            """
                            pendingCommands = cmdmgr.getPendingCommands()
                            print("Comandos pendientes de envio: ", pendingCommands.count())
                            s.send(('-SIN COMANDOS-'+str(i)).encode())
                            i = i + 1
                                
                            for com in pendingCommands:
                                print("Se hardcodea ejecucion comando ", str(com.pk))
                                Arreglar aca, hay un problema con binarycmd!
                                s.send(com.binarycmd)
                                print("Comando ", com.binarycmd, " enviado")
                                
                                
                                com.setExecuted()
                                """
                                TODO: Encodear y mandar al satelite por el mismo socket aca!
                                """
                            
                            
                    finally:
                        s.close()
                        
                
                except Exception as err:
                    Log.create("ERROR TlmyCmdProcessor", "Error/Exception "+str(err), module, Log.ERROR).save()
                    #TODO, quitar print
                   
                   
                    print(str(datetime.datetime.utcnow()), err)
                    unconnectionLimit = unconnectionLimit + 1
                     
                except IOError as err2:
                    Log.create("IOERROR TlmyCmdProcessor", "Error/Exception "+str(err2), module, Log.ERROR).save()
                    #TODO, quitar print
                    
                    print(str(datetime.datetime.utcnow()), err2)
                    unconnectionLimit = unconnectionLimit + 1
                  
                print("Sleeping..")
                time.sleep(int(DISCONNECTION_SLEEP))
                    
    except ValueError as ve:
        Log.create("Failed connection..", "Error/Exception "+str(ve), module, Log.ERROR).save()
        print("Failed connection..")
        
    print("Finalized")
    
        
    

        