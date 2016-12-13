'''
Created on 25 de nov. de 2016

@author: pabli
'''
from Calibration.BaseCalibration import BaseCalibration




class GCalibration(BaseCalibration):
    def duplicateAndSum(self, raw):
        return raw*0.2 + 1

    def linealCalibration(self, raw):
        return raw*0.2 + 1
    
    def cuadraticCalibration(self, raw):
        #return raw**2 - 10*raw + 3
        #Cambio la cuadratica por una lineal para que no se me vaya de rango
        return raw*0.2 + 1
    
    def LeftPanelTempCalibration(self, raw):
        #return raw**2 - 10*raw + 3
        #Cambio la cuadratica por una lineal para que no se me vaya de rango
        return raw*0.1 + 1
    
        
    def RightPanelTempCalibration(self, raw):
        #return raw**2 - 10*raw + 3
        #Cambio la cuadratica por una lineal para que no se me vaya de rango
        return raw*0.1 + 1
    
    def SolarSensorACalibration(self, raw):
        #return raw**2 - 10*raw + 3
        #Cambio la cuadratica por una lineal para que no se me vaya de rango
        return raw*0.1 + 1
    
    
    
    def discretCalibration(self, raw):
        if raw<0:
            return 0
        elif raw<10:
            return 5
        else:
            return 20
        
        
