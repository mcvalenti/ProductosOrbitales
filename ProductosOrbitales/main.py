'''
Created on 10/08/2017

@author: mcvalenti
'''
import numpy as np
from datetime import datetime, timedelta
import csv
import ephem
from ephem import degree
from TLE import Tle
from Sitio import Sitio
from Satellite import Satellite

def calcula_pasada(sat,obs,startTime,stopTime):
    pass_time=startTime
    with open('validaciones/pasadas.csv', 'w') as csvfile: #csv
        fieldnames = ['Pasada','rise_time','rise_azimuth','max_elev_time','max_elev','set_time','set_azimuth','duracion'] #csv 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)   #csv 
        writer.writeheader()       #csv
        n=0
        while pass_time < stopTime:
            obs.sitio.date=pass_time
            rise_time,rise_azimuth,max_elev_time,max_elev,set_time,set_azimuth=obs.sitio.next_pass(sat.sat)
            pass_duration=(set_time-rise_time)*1440
            print rise_time.datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),rise_azimuth,max_elev_time,max_elev,set_time,set_azimuth, pass_duration
            writer.writerow({'Pasada':n,'rise_time':rise_time.datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),'rise_azimuth':rise_azimuth/degree,'max_elev_time':max_elev_time.datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),'max_elev':max_elev/degree,'set_time':set_time.datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),'set_azimuth':set_azimuth/degree,'duracion':pass_duration}) #csv
            pass_time=set_time.datetime()
            n=n+1
    return {}

def calcula_eclipse(sat,obs,startTime,stopTime):
    prop_time=startTime
    sat.sat.compute(prop_time)
    in_eclipse=sat.sat.eclipsed
    eclipse_state=[in_eclipse]
    n=1
    m=0
    with open('validaciones/eclipses.csv', 'w') as csvfile: #csv
        fieldnames = ['Eclipse','inicio','fin','duracion'] #csv
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  #csv  
        writer.writeheader() #csv
        while prop_time < stopTime:
            sat.sat.compute(prop_time)
            in_eclipse=sat.sat.eclipsed
            eclipse_state.append(in_eclipse)
            if in_eclipse and eclipse_state[m]==False:
                eclipse_ini=prop_time
                n=n+1            
            elif in_eclipse==False and eclipse_state[m]==True:
                eclipse_fin=prop_time
                duration=(eclipse_fin-eclipse_ini).total_seconds()/60.0
                print 'Eclipse '+str(n)+': '+'inicia: '+eclipse_ini.strftime('%Y-%m-%d %H:%M:%S')+' '+'finaliza: '+eclipse_fin.strftime('%Y-%m-%d %H:%M:%S')+' duarcion: '+str(duration)+'\n'
                writer.writerow({'Eclipse':n,'inicio': eclipse_ini.strftime('%Y-%m-%d %H:%M:%S'), 'fin': eclipse_fin.strftime('%Y-%m-%d %H:%M:%S'), 'duracion':duration}) #csv
            m=m+1
            prop_time=prop_time+timedelta(seconds=1)
    return {}

def calcula_track(sat,startTime,stopTime):
    
    prop_time=startTime
    lon_lat_track=open('validaciones/lon_lat.dat','w')
    with open('validaciones/tracks.csv', 'w') as csvfile: #csv
        fieldnames = ['Epoca','Longitud','Latitud'] #csv 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)   #csv 
        writer.writeheader()       #csv 
        while prop_time < stopTime:
            sat.sat.compute(prop_time)
            writer.writerow({'Epoca': prop_time.strftime('%Y-%m-%d %H:%M:%S'), 'Longitud': sat.sat.sublong/degree, 'Latitud':sat.sat.sublat/degree}) #csv
            lon_lat_track.write(str(sat.sat.sublong/degree)+' '+str(sat.sat.sublat/degree)+'\n')
            prop_time=prop_time+timedelta(minutes=1) 
    lon_lat_track.close()
    return {}

if __name__=='__main__':

    """
    Utiliza la libreria PyEphem para los calculos de las pasadas por los sitios, 
    las proyecciones de las orbitas en Tierra o Tracks, y los eclipses y luego valida con
    STK. 
    """
    #====================
    # Periodo de Analisis
    #====================
    startTime=datetime(2017,3,8,0,0,0)
    stopTime=datetime(2017,3,9,0,0,0)
    
    #====================
    # Tle satelite SAC-D
    #====================
    tle_archivo='tles/SACD_8_3_2017.tle'
#    tle_archivo='tles/25544_enero_2017.tle'
    tle=Tle.creadoxArchivo(tle_archivo)
    P=(86400.0/float(tle.n))
    print 'periodo orbital = ',P
    vel=360.0*60/(2*P)
    print 'vel orbital = ',vel
    
    #====================
    # Objetos de PyEphem
    #====================
    # Satellite (Body)
    sat = Satellite.creadoxTle("SAC-D",tle.linea1,tle.linea2)
#    sat=ephem.readtle("ISS",tle.linea1,tle.linea2)
    # SITIO (Observer)
    obs=Sitio('-31.5241','-64.4635',0,'-0:34',startTime)
#     obs=ephem.Observer()
#     obs.lat='-31.5241'
#     obs.lon='-64.4635'
#     obs.pressure=0
#     obs.horizon='-0:34'
    
#     while startTime < stopTime:
#         obs.date=startTime
#         rise_time,rise_azimuth,max_elev_time,max_elev,set_time,set_azimuth=obs.next_pass(sat)
#         print rise_time,set_time,(set_time-rise_time)*1440
#         startTime=set_time.datetime()
    
    #==============================================================
    # PASADAS
    #==============================================================
    calcula_pasada(sat, obs, startTime, stopTime)
    
    #==============================================================
    # Eclipses
    #==============================================================
#    calcula_eclipse(sat, obs, startTime, stopTime)
    
    #==============================================================
    # Tracks
    #==============================================================  
#    calcula_track(sat,startTime,stopTime)



        
        
        

    
    