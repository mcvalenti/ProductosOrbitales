'''
Created on 10/08/2017

@author: mcvalenti
'''
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import csv
import ephem
from ephem import degree
from TLE import Tle
from Sitio import Sitio
from Satellite import Satellite

def calcula_pasada(sat,obs,startTime,stopTime):
    """
    A partir del sitio de observacion y el satelite.
    Calcula las pasadas del satelite por el sitio, para
    un dado intervalo [startTime:stopTime]
    ---------------------------------------------------
    Devuleve dos listas con los instantes de salida y
    puesta.
    Genera un archivo con extension csv con los registros
    de las pasadas. 
    """
    pass_time=startTime
    with open('validaciones/pasadas.csv', 'w') as csvfile: #csv
        fieldnames = ['Pasada','rise_time','rise_azimuth','max_elev_time','max_elev','set_time','set_azimuth','duracion'] #csv 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)   #csv 
        writer.writeheader()       #csv
        n=0
        rise_time_list=[]
        set_time_list=[]
        while pass_time < stopTime:
            obs.sitio.date=pass_time
            rise_time,rise_azimuth,max_elev_time,max_elev,set_time,set_azimuth=obs.sitio.next_pass(sat.sat)
            pass_duration=(set_time-rise_time)*1440
            print rise_time.datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),rise_azimuth,max_elev_time,
            max_elev,set_time,set_azimuth, pass_duration
            writer.writerow({'Pasada':n,'rise_time':rise_time.datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),'rise_azimuth':rise_azimuth/degree,'max_elev_time':max_elev_time.datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),'max_elev':max_elev/degree,'set_time':set_time.datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),'set_azimuth':set_azimuth/degree,'duracion':pass_duration}) #csv
            rise_time_list.append(rise_time)
            set_time_list.append(set_time)
            pass_time=set_time.datetime()
            n=n+1
    return rise_time_list, set_time_list

def calcula_eclipse(sat,startTime,stopTime):
    """
    Calcula los intervalos en que el satelite indicado se 
    encuentra en situacion de eclipse durante el periodo 
    de analisis [startTime:stopTime]
    -----------------------------------------------------
    Genera un archivo con extension csv con los registros 
    de los eclipses
    """
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
    """
    Calcula las coordenadas geodesicas de las trayectorias
    del satelite para el intervalo de analisis [starTime:stopTime]
    ---------------------------------------------------------------
    Devuelve un set de datos con todas las longitudes y latitudes 
    de las orbitas. 
    """
    prop_time=startTime.datetime()
    lon_lat_track=open('validaciones/lon_lat.dat','w')
    set_datos=[]
    lat=[]
    lon=[]
    with open('validaciones/tracks.csv', 'w') as csvfile: #csv
        fieldnames = ['Epoca','Longitud','Latitud'] #csv 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)   #csv 
        writer.writeheader()       #csv 
        while prop_time < stopTime.datetime():
            sat.sat.compute(prop_time)
            writer.writerow({'Epoca': prop_time.strftime('%Y-%m-%d %H:%M:%S'),
                              'Longitud': sat.sat.sublong/degree,
                               'Latitud':sat.sat.sublat/degree}) #csv
            lon_lat_track.write(str(sat.sat.sublong/degree)+' '+str(sat.sat.sublat/degree)+'\n')
            lat.append(sat.sat.sublat/degree)
            lon.append(sat.sat.sublong/degree)
            prop_time=prop_time+timedelta(seconds=1)  
    lon_lat_track.close()
    set_datos=[lon,lat]
    return set_datos

def grafica_track_pasada(sitio_lon,sitio_lat,set_datos_lista):
    """
    Utiliza la biblioteca Basemap de Python para ofrecer una
    representacion grafica de la trayectoria en la superficie
    terrestre solo cuando el satelite esta en visibilidad, 
    es decir de las pasadas por el sitio de interes. 
    """
    # miller projection
    map = Basemap(projection='ortho', 
              lat_0=sitio_lat, lon_0=sitio_lon)
    map.bluemarble()
    date = datetime.utcnow() 
    x0,y0=map(sitio_lon,sitio_lat)
    plt.text(x0,y0,'CETT',fontsize=12,fontweight='bold',color='yellow')
    map.plot(x0,y0,marker='D',color='yellow')
    for m in range(len(set_datos_lista)):
        x, y = map(set_datos_lista[m][0],set_datos_lista[m][1])
        map.scatter(x,y,2,marker='o',color='red')
    plt.title('Proyeccion')
    plt.show()
    
def coord_Geodesicas(sat,prop_time,stopTime):
    
    with open('validaciones/coordGeod_noaa.csv', 'w') as csvfile: #csv
        fieldnames = ['Epoca','Longitud','Latitud'] #csv 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)   #csv 
        writer.writeheader()       #csv 
        while prop_time < stopTime:
            sat.sat.compute(prop_time)
            writer.writerow({'Epoca': prop_time.strftime('%Y-%m-%d %H:%M:%S'),
                              'Longitud': sat.sat.sublong/degree,
                               'Latitud':sat.sat.sublat/degree}) #csv            
            prop_time=prop_time+timedelta(minutes=1)
    return {}

if __name__=='__main__':

    """
    Utiliza la libreria PyEphem para los calculos de las pasadas por los sitios, 
    las proyecciones de las orbitas en Tierra o Tracks, y los eclipses. 
    """
    #====================
    # Periodo de Analisis
    #====================
    startTime=datetime(2017,3,8,0,0,0)
    stopTime=datetime(2017,3,9,23,59,59)
#     startTime=datetime(1991,1,1,0,0,0)
#     stopTime=datetime(1991,1,1,23,59,59)
    
    #====================
    # Tle satelite SAC-D
    #====================
    tle_archivo='tles/SACD_8_3_2017.tle'
#    tle_archivo='tles/noaa10_16969_1_1_1991.tle'
    tle=Tle.creadoxArchivo(tle_archivo)
    
    #====================
    # Objetos de PyEphem
    #====================
    # Satellite (Body)
    sat = Satellite.creadoxTle("SAC-D",tle.linea1,tle.linea2)
    # SITIO (Observer)
    sitio_lat=-31.5241
    sitio_lon=-64.4635
    obs=Sitio(str(sitio_lat),str(sitio_lon),0,'-0:34',startTime)
    
    #==============================================================
    # PASADAS
    #==============================================================
    rise_time_list, set_time_list=calcula_pasada(sat, obs, startTime, stopTime)
    
    #==============================================================
    # Tracks de pasadas
    #==============================================================
    set_datos_lista=[]
    n=0
    for rt in rise_time_list: 
        st=set_time_list[n]
        set_datos=calcula_track(sat,rt,st)
        set_datos_lista.append(set_datos)
        n=n+1
    grafica_track_pasada(sitio_lon,sitio_lat,set_datos_lista)
    
    #==============================================================
    # Coordenadas Geodesicas
    #==============================================================
    coord_Geodesicas(sat,startTime,stopTime) 
    
    #==============================================================
    # Eclipses
    #==============================================================
    calcula_eclipse(sat,startTime, stopTime)



    


        
        
        

    
    