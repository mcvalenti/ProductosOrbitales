import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from datetime import datetime
# miller projection
map = Basemap(projection='mill',lon_0=0)
# plot coastlines, draw label meridians and parallels.
map.drawcoastlines()
map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])
# fill continents 'coral' (with zorder=0), color wet areas 'aqua'
map.drawmapboundary(fill_color='blue')
map.fillcontinents(color='green',lake_color='aqua')
# shade the night areas, with alpha transparency so the
# map shows through. Use current time in UTC.
date = datetime.utcnow()
CS=map.nightshade(date)

# puntos sobre el mapa
lats = []
lons = []
arch=open('validaciones/lon_lat.dat','r')
lineas=arch.readlines()
for li in lineas:
    campos=li.split()
    lons.append(float(campos[0]))
    lats.append(float(campos[1]))
x, y = map(lons,lats)
map.scatter(x,y,3,marker='o',color='red')
plt.title('Mapitas')
plt.show()