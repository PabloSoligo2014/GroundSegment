'''
Created on 25 de nov. de 2016

@author: pabli
'''
from Calibration.BaseCalibration import BaseCalibration




class GCalibration(BaseCalibration):
    def duplicateAndSum(self, raw):
        return raw*2 + 0.5

    def linealCalibration(self, raw):
        return raw*0.2 + 1
    
    def cuadraticCalibration(self, raw):
        return raw**2 + 5*raw + 3
    
    def discretCalibration(self, raw):
        if raw<0:
            return 0
        elif raw<10:
            return 5
        else:
            return 20
        
        
