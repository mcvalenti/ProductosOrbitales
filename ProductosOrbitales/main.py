'''
Created on 10/08/2017

@author: mcvalenti
'''
from datetime import datetime, timedelta
import ephem
from TLE import Tle


def calcula_pasada():
    pass

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
    startTime=datetime(2017,3,6)
    stopTime=datetime(2017,3,28)
    
    #====================
    # Tle satelite SAC-D
    #====================
    tle_archivo='tles/SACD_8_3_2017.tle'
    tle=Tle.creadoxArchivo(tle_archivo)
    
    
    #====================
    # Objetos de PyEphem
    #====================
    # SITIO
    ETC= ephem.Observer()
    ETC.lon, ETC.lat = '-64.463522', '-31.524075'
    ETC.pressure = 0 # fundamental para que coincida con STK
    ETC.horizon = '-0:34' # fundamental para que coincida con STK
    ETC.date=startTime
    # Satellite (Body)
    sat = ephem.readtle("SAC D",tle.linea1,tle.linea2)
    #==============================================================
    # PASADAS
    #==============================================================
#     pass_time=startTime
#     while pass_time < stopTime:
#         ETC.date=startTime
#         rise_time,rise_azimuth,max_elev_time,max_elev,set_time,set_azimuth=ETC.next_pass(sat)
# #        print rise_time,rise_azimuth,max_elev_time,max_elev,set_time,set_azimuth
#         pass_time=set_time.datetime()
    #==============================================================
    # Eclipses
    #==============================================================
    prop_time=startTime
    sat.compute(prop_time)
    in_eclipse=sat.eclipsed
    eclipse_date_list=[]
    while prop_time < stopTime:
        sat.compute(prop_time)
#         in_eclipse=sat.comput(prop_time).eclipsed
#         if in_eclipse:
#             eclipse_date_list.append(prop_time)
        print prop_time, sat.sublong, sat.sublat
        prop_time=prop_time+timedelta(minutes=1)

    
    