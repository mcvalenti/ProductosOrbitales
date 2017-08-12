'''
Created on 12 ago. 2017

@author: ceci
'''
import ephem

class Sitio:
    '''
    classdocs
    '''

    def __init__(self,lat,lon,pressure,horizon,date):
        '''
        Constructor
        '''
        self.sitio = ephem.Observer()
        self.sitio.lon= lon
        self.sitio.lat= lat
        self.sitio.pressure = pressure
        self.sitio.horizon= horizon
        self.sitio.date = date
