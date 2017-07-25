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
from _struct import unpack, pack
from array import array
import binascii






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



def __showAsHex(ba):
    
    result = ""
    for b in ba:
        result = result+hex(b)+" "
     
    return result

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


    
    """Funcion principal del servicio, aplicacion encargada de decodificar, transformar y persistir la telemetria del satelite y de codificar y transmitir los 
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
    from GroundSegment.Utils.Console import Console, NORMAL, WARNING, ERROR
    
   
    
    try:
        #Si me desconecto intento nuevamente conectarme despues de un sleep
        #y asi in eternum....
        
        Console.log("Reading configuration..")
        
        
        from GroundSegment.models.Satellite import Satellite
        from GroundSegment.models.UHFRawData import UHFRawData
        from GroundSegment.models.Parameter import Parameter
        from GroundSegment.models.TlmyVarType import TlmyVarType
        from GroundSegment.models.Log import Log
        from GroundSegment.models.Watchdog import Watchdog
        from GroundSegment.Utils.Utils import *
        from GroundSegment.models.DownlinkFrame import DownlinkFrame 
        from GroundSegment.Managers.CommandManager import CommandManager
        from GroundSegment.Utils.BColor import bcolors
        
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
            
            """Deprecated, ahora el ip/puerto del cortex o equipo UHF es atributo del satelite"""
            uhfServerIp             = loadOrCreateParam("UHF_SERVER_IP", "GroundStation", "127.0.0.1", "IP del servidor TCP de la antena UHF")
            uhfServerPort           = loadOrCreateParam("UHF_SERVER_PORT", "GroundStation", "3210", "Puerto del servidor TCP de la antena UHF")    
            
            
            BUFFER_SIZE             = loadOrCreateParam("UHF_BUFFER_SIZE", "GroundStation", "1024", "Tamanio del buffer del cliente TCP")
            DISCONNECTION_SLEEP     = loadOrCreateParam("UHF_DISCONNECTION_SLEEP", "GroundStation", "10", "Tiempo en que se duerme la aplicacion ante una desconexion a la espera de volver a intentar")
            cls()
            Console.log("Done..trying to connect ip "+uhfServerIp+" ,port "+uhfServerPort)
            
            unconnectionLimit       = 0
            i = 0
            while unconnectionLimit<10:
                cls()
                Console.log("Create o recreate socket...", str(datetime.datetime.utcnow()))
                
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
                    socket.setdefaulttimeout(5.0)
                    s.connect( (sat.commServerIP, int(sat.commServerPort)) )
                    
                    try:
                        Console.log("Successfully connection to.."+uhfServerPort)
                        while True:
                            try:
                                """
                                Establezco un timeout para la bajada, con o sin bajada los comandos deben ser enviados
                                """
                                #s.settimeout(5.0)
                                
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
                                    #print("Socket connection broken")
                                    raise RuntimeError("socket connection broken")
                                else:
                                    """
                                    Me guardo el crudo tal cual llego antes de procesarlo, la tabla donde se guarda es UHFRawData
                                    """
                                    os.system('cls||clear')
                                    Console.log("--------------------Data Received-------------------")
                                    Console.log("Data length:"+str(len(chunk)))
                                    
                                    #print("\nData Received("+str(timezone.datetime.utcnow() )+"), Tamano: ", , "\nData->", chunk)
                                    
                                    data = UHFRawData()
                                    data.source = source
                                    data.data = chunk
                                    data.processed = False
                                    data.save()
                                    
                                    startproctime = timezone.now()
                                    
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
                                    
                                    #A8 A4 B0 AA AC 40 60 40 40 40 40 40 40 E1 03 F0 02 03 83 A5
                                         
                                    vardataoffset = 7+7+1+1
                                    payload = ax25[ vardataoffset: ]
                                    
                                    pn = unpack("<H",  payload[1:3])
                                    Console.log("Packet number: "+str(pn))
                                    
                                    
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
                                    
                                    Console.log("Data processed("+str(timezone.datetime.utcnow() )+")")
                                    
                                    data.processed = True
                                    data.processedTime = (timezone.now()-startproctime).total_seconds() 
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
                                    #print("Send harcode command")
                                    
                                    #header =  b'\x56\xA8\xA4\xB0\xAA\xAC\x40\x60\x40\x40\x40\x40\x40\x40\xE1\x03\xF0'
                                    #pkt = b'\x56\xA8\xA4\xB0\xAA\xAC\x40\x60\x40\x40\x40\x40\x40\x40\xE1\x03\xF0\x17\x00\x00\x00\x02\x02'
                                    #sentbytes = s.send(pkt)
                                    
                                    
                                    #Aca esta la posta: https://www.qb50.eu/index.php/tech-docs/category/16-archive?download=19:scs-docs
                                    #1- 7 bytes - Destination Callsign
                                    #2- 7 bytes - Source Callsign
                                    #3- 2 bytes - Control Bytes
                                    #4- Variable - Data bytes (Data sent by the OBC)
                                    #5- 2 bytes - FCS (AX25 CRC)
                                    """
                                    destination  = ax25[0:7]
                                    asource      = ax25[7:7+7]
                                    control      = ax25[7+7:7+7+1]
                                    protocol     = ax25[7+7+1:7+7+1+1]
                                    vardataoffset = 7+7+1+1
                                    payload = ax25[ vardataoffset: ]
                                    """
                                    ilen = len(asource+destination+control+protocol+pack('BB', 2, 2 ))+4
                                    pkt = b'\x56'+pack('>I', ilen)+asource+destination+control+protocol+pack('BB', 2, 2 )     
                                    __showAsHex(pkt)
                                    
                                    crc = binascii.crc_hqx(pkt, 0)
                                    pcrc = pack('H', crc)
                                    
                                    
                                    #Este calcula el CRC-CCITT (XModem)
                                    #__showAsHex(pack('H', binascii.crc_hqx(b'\xA8\xA4\xB0\xAA\xAC\x40\x60\x40\x40\x40\x40\x40\x40\xE1\x03\xF0\x02\x02', 0)))
                                    
                                    #Este calcula CRC 16 pelado
                                    #__showAsHex(pack('H', binascii.crc_hqx(b'\xA8\xA4\xB0\xAA\xAC\x40\x60\x40\x40\x40\x40\x40\x40\xE1\x03\xF0\x02\x02', 0)))
                                    
                                    #'A8 A4 B0 AA AC 40 60 40 40 40 40 40 40 E1 03 F0 02 02 0A B4'
                                    #sentbytes = s.send(b'\x56\xA8\xA4\xB0\xAA\xAC\x40\x60\x40\x40\x40\x40\x40\x40\xE1\x03\xF0\x02\x02')
                                    #ISO 3309 (HDLC) Recommendations
                                    #https://www.tapr.org/pdf/AX25.2.2.pdf
                                    #Este guacho no rompe la conexion
                                    #sentbytes = s.send(b'\x56\x07\x00\x00\x00\x02\x02')
                                    
                                    
                                    #pkt = b'\x56\xA8\xA4\xB0\xAA\xAC\x40\x60\x40\x40\x40\x40\x40\x40\xE1\x03\xF0\x02\x02'
                                    #sentbytes = s.send(pkt)
                                    #sentbytes = s.send(pack('BIBB', 56, 3, 2, 2 ))
                                    
                                    
                                    
                                    print("hardcode command, bytes sent :", sentbytes )
                                    
                                      
                                ##f.close()
                            except socket.timeout:
                                #Error de timeout de sockets, si el satelite esta en linea 
                                Console.log("Socket timeout", WARNING)
                               
                                
                            """
                            Si el satelite esta en linea debo mandar comandos pendientes
                            """
                            pendingCommands = cmdmgr.getPendingCommands()
                            #Console.log("Comandos pendientes de envio: "+str(pendingCommands.count()))
                            
                            
                            #s.send(('-SIN COMANDOS-'+str(i)).encode())
                            i = i + 1
                                
                            for com in pendingCommands:
                                
                                Console.log("Se hardcodea ejecucion comando "+str(com.pk))
                                #freq                = unpack("<d", chunk[PosFrequency:PosFrequency+LenFrequency])
                                
                                #oframecommand = pack('c', 56)
                                #cmd = com.getBinaryCommand()
                                #opayload = pack('c', 2, cmd[1])
                                
                                #a = array('b', )
                                
                                #s.send(com.getBinaryCommand())
                                
                                
                                #s.send(pack('cIcc', b'a', 7 ,b'2', b'2'))
                                
                                
                                
                                Console.log("Comando "+str(com.binarycmd)+" enviado")
                                
                                
                                com.setExecuted()
                                """
                                TODO: Encodear y mandar al satelite por el mismo socket aca!
                                """
                            
                            
                    finally:
                        s.close()
                        
                
                except Exception as err:
                    Log.create("ERROR TlmyCmdProcessor", "Error/Exception "+str(err), module, Log.ERROR).save()
                    #TODO, quitar print
                   
                    Console.log(err.__str__(), WARNING)
                    
                    unconnectionLimit = unconnectionLimit + 1
                     
                except IOError as err2:
                    Log.create("IOERROR TlmyCmdProcessor", "Error/Exception "+str(err2), module, Log.ERROR).save()
                    #TODO, quitar print
                    Console.log(err2.__str__(), WARNING)
                    unconnectionLimit = unconnectionLimit + 1
                  
                
                Console.log("Sleeping")
                time.sleep(int(DISCONNECTION_SLEEP))
                    
    except ValueError as ve:
        Log.create("Failed connection..", "Error/Exception "+str(ve), module, Log.ERROR).save()
        print("Failed connection..")
        
    print("Finalized")
    
        
    

        