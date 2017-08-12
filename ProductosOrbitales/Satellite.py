'''
Created on 12 ago. 2017

@author: ceci
'''
import ephem

class Satellite(object):
    '''
    classdocs
    '''
    @classmethod    
    def creadoxTle(cls,name, tleline1,tleline2):
        result=cls()
        result.name=name
        result.tleline1=tleline1
        result.tleline2=tleline2
        result.sat = ephem.readtle(result.name,result.tleline1,result.tleline2)
        
        return result