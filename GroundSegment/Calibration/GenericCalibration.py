'''
Created on 25 de nov. de 2016

@author: pabli
'''
from Calibration.BaseCalibration import BaseCalibration




class GCalibration(BaseCalibration):
    def duplicateAndSum(self, raw):
        return raw*0.2 + 1

    def linealCalibration(self, obj, raw):
        return raw*obj.coefficients.get(code="GAIN").value + obj.coefficients.get(code="OFFSET").value

    
    def cuadraticCalibration(self, obj, raw):
        #return raw**2 - 10*raw + 3
        #Cambio la cuadratica por una lineal para que no se me vaya de rango
        return raw*0.2 + 1
    
    def LeftPanelTempCalibration(self, obj, raw):
        #return raw**2 - 10*raw + 3
        #Cambio la cuadratica por una lineal para que no se me vaya de rango
        return raw*0.1 + 1
    
        
    def RightPanelTempCalibration(self, obj, raw):
        #return raw**2 - 10*raw + 3
        #Cambio la cuadratica por una lineal para que no se me vaya de rango
        return raw*0.1 + 1
    
    def SolarSensorACalibration(self, obj, raw):
        #return raw**2 - 10*raw + 3
        #Cambio la cuadratica por una lineal para que no se me vaya de rango
        return raw*0.1 + 1
    
    def antSACalib(self, obj,  raw):
        return 0.001
    
    
    def discretCalibration(self, obj, raw):
        if raw<0:
            return 0
        elif raw<10:
            return 5
        else:
            return 20
        
        
