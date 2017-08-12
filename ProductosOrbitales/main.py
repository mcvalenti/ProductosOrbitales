'''
Created on 10/08/2017

@author: mcvalenti
'''
from datetime import datetime, timedelta
import ephem
from TLE import Tle
from Sitio import Sitio
from Satellite import Satellite

def calcula_pasada(sat,obs,startTime,stopTime):
    pass_time=startTime
    while pass_time < stopTime:
        obs.sitio.date=startTime
        rise_time,rise_azimuth,max_elev_time,max_elev,set_time,set_azimuth=obs.sitio.next_pass(sat.sat)
        print rise_time,rise_azimuth,max_elev_time,max_elev,set_time,set_azimuth
        pass_time=set_time.datetime()
    return {}

def calcula_eclipse():
    pass

def calcula_track():
    pass


if __name__=='__main__':

    """
    Utiliza la libreria PyEphem para los calculos de las pasadas por los sitios, 
    las proyecciones de las orbitas en Tierra o Tracks, y los eclipses y luego valida con
    STK. 
    """
    #====================
    # Periodo de Analisis
    #====================
    startTime=datetime(2017,1,1,0,0,0)
    stopTime=datetime(2017,1,2,1,0,0)
    
    #====================
    # Tle satelite SAC-D
    #====================
#    tle_archivo='tles/SACD_8_3_2017.tle'
    tle_archivo='tles/25544_enero_2017.tle'
    tle=Tle.creadoxArchivo(tle_archivo)
    
    
    #====================
    # Objetos de PyEphem
    #====================
    # Satellite (Body)
    sat = Satellite.creadoxTle("SAC D",tle.linea1,tle.linea2)
    # SITIO (Observer)
    obs=Sitio('-64.463522','-31.524075',0,'-0:34',startTime)
    
    #==============================================================
    # PASADAS
    #==============================================================
    calcula_pasada(sat, obs, startTime, stopTime)
    
    #==============================================================
    # Eclipses
    #==============================================================
    prop_time=startTime
    sat.compute(prop_time)
    in_eclipse=sat.eclipsed
    eclipse_registrer=[]
    eclipse_state=[in_eclipse]
    n=1
    m=0
    while prop_time < stopTime:
        sat.compute(prop_time)
        in_eclipse=sat.eclipsed
        eclipse_state.append(in_eclipse)
        if in_eclipse and eclipse_state[m]==False:
            eclipse_ini=prop_time
            n=n+1            
        elif in_eclipse==False and eclipse_state[m]==True:
            eclipse_fin=prop_time
            duration=(eclipse_fin-eclipse_ini).total_seconds()/60.0
            print 'Eclipse '+str(n)+': '+'inicia: '+eclipse_ini.strftime('%Y-%m-%d %H:%M:%S')+' '+'finaliza: '+eclipse_fin.strftime('%Y-%m-%d %H:%M:%S')+' duarcion: '+str(duration)+'\n'

        m=m+1
        prop_time=prop_time+timedelta(seconds=1)
    
    #==============================================================
    # Tracks
    #==============================================================    
    
#         sat.compute(prop_time)
# #         in_eclipse=sat.comput(prop_time).eclipsed
# #         if in_eclipse:
# #             eclipse_date_list.append(prop_time)
#         print prop_time, sat.sublong, sat.sublat

        
        

    
    