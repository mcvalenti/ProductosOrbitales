"""
Created on Sun Apr 10 19:19:04 2016

GAUSS METHOD OF PRELIMINARY ORBIT DETERMINATION.

Dados los cosenos directores rho1, rho2, rho3 y 
las posiciones de la estacion R1, R2 y R3 para los tiempos
t1, t2 y t3.
Se calculan los elementos orbitales. 

@author: mcvalenti
"""
import numpy as np
import matplotlib.pyplot as plt

mu=398600 # [km3/s2]
Re=6368 # [km]
f=0.003353
pi=np.pi
rad=pi/180.0

"""
################################################################
# EJEMPLO - 5.11 CURTIS -
Conocidos los tiempos sidereos de observacion y las coordenadas
 celestes (topocentricas) de apuntamiento de la antena para 3 
instantes de tiempo se determina la posicion del satelite para 
esos tres momentos de observacion
################################################################
"""
phi=40.0*rad# [grados]
H=1 # [m]
ts=[44.506*rad,45.0*rad,45.499*rad]
alpha=[43.537*rad,54.420*rad,64.318*rad]
delta=[-8.7833*rad,-12.074*rad,-15.105*rad]
#-------------------------

def estacion(phi,H,ts):
    Re=6378 # [km]
    f=0.003353
    factor=((Re/np.sqrt(1-(2*f-f*f)*np.sin(phi)*np.sin(phi)))+H)
    i=factor*np.cos(phi)*np.cos(ts)
    j=factor*np.cos(phi)*np.sin(ts)
    factor2=(((Re*(1-f)*(1-f))/np.sqrt(1-(2*f-f*f)*np.sin(phi)*np.sin(phi)))+H)
    k=factor2*np.sin(phi)
    return i,j,k
    
def cosendire(alpha,delta):
    rho=[np.cos(delta)*np.cos(alpha),np.cos(delta)*np.sin(alpha),np.sin(delta)]
    return rho    
"""
Coordenadas de Estacion.
"""
print '################################################'
print 'COORDENADAS DE LA ESTACION PARA LOS T1, T2, T3'
print '################################################'
R1=np.array(estacion(phi,H,ts[0]))
R2=np.array(estacion(phi,H,ts[1]))
R3=np.array(estacion(phi,H,ts[2]))
print R1
print R2
print R3
print '################################################'
"""
Cosenos directores
"""
rho1=cosendire(alpha[0],delta[0])
rho2=cosendire(alpha[1],delta[1])
rho3=cosendire(alpha[2],delta[2])

print 'COSENOS DIRECTORES'
print '################################################'
print rho1
print rho2
print rho3

"""
Resolucion del Algoritmo
"""

# STEP 1 - Tiempos.

t1=0.0
t2=118.10
t3=237.58
print '################################################'
print 'Intervalos de tiempo entre observaciones [seg]'
tau1=t1-t2
tau3=t3-t2
tau=t3-t1
print tau1, tau3, tau
print '################################################'

# STEP 2 - Productos Vectoriales
p1=np.cross(rho2,rho3)
p2=np.cross(rho1,rho3)
p3=np.cross(rho1,rho2)
print 'Productos Vectoriales'
print p1
print p2
print p3
print '################################################'

# STEP 3 - D0
D0=np.dot(rho1,p1)
print 'D0= '+str(D0)
print '################################################'

# STEP 4 - MATRIZ D
print 'MATRIZ D'
D=np.array([[np.dot(R1,p1),np.dot(R1,p2),np.dot(R1,p3)],
     [np.dot(R2,p1),np.dot(R2,p2),np.dot(R2,p3)],
      [np.dot(R3,p1),np.dot(R3,p2),np.dot(R3,p3)]])  
print D      
print '################################################'

# STEP 5 -Coeficientes A y B. 
term1=-D[0][1]*tau3/tau
term2=D[2][1]*tau1/tau
A=(1.0/D0)*(term1+D[1][1]+term2)
print tau1,D[0][1],D[1][1],D[2][1]
print 'A = '+str(A)+' km'

term3=D[0][1]*(tau3*tau3-tau*tau)*(tau3/tau)
term4=D[2][1]*(tau*tau-tau1*tau1)*(tau1/tau)
B=(1.0/(6*D0))*(term3+term4)
print 'B = '+str(B)+' km-s2'

print '################################################'

# STEP 6

E=np.dot(R2,rho2)
R2cuad=np.dot(R2,R2)
print 'E= '+str(E) +' km'
print 'R2 cuadrado = '+str(R2cuad)+' km2'

print '################################################'

# STEP 7

amin=-(A*A+2*A*E+R2cuad)
bmin=-2*mu*B*(A+E)
cmin=-mu*mu*B*B
print 'COEFICIENTES DEL POLINOMIO'
print 'a = '+str(amin)+' km2'
print 'b = '+str(bmin)+' km5'
print 'c = '+str(cmin)+' km8'

print '################################################'

'''
# STEP 8 Hallar la raiz de x8+ax7+bx3+c=0 -
# Metodo de Newton.
# Para obtener la condicion inicial graficamos.

#y=[]
#for x in range(10000):
#    f=x**8+amin*x**6+bmin*x**3+cmin
#    y.append(f)
#x=range(10000)    
#plt.figure()
#plt.plot(x, y)
#plt.show()
#plt.grid()   
'''

def newton(xini,amin,bmin,cmin):
    xfin=0.0      
    itera=0.0
    dif=abs(xfin-xini)
    while dif>0.2:#:
        itera += 1        
        num=xini**8+amin*xini**6+bmin*xini**3+cmin
        denom=8*xini**7+6*amin*xini**5+3*bmin*xini*xini
        xfin=xini-(num/denom)
        dif=abs(xfin-xini)
        print itera, xfin
        xini=xfin        
    return xini

xini=9000.0 # se determina observando el grafico. 
r2min=newton(xini,amin,bmin,cmin)
print 'Resultado de la distancia geocentrica del Satelite'
print 'r2= '+str(r2min)

print '################################################'

# STEP 9 Slant ranges srho1, srho2, srho3
term5=6*(D[2][0]*(tau1/tau3)+D[1][0]*(tau/tau3))*r2min**3
term6=mu*D[2][0]*(tau*tau-tau1*tau1)*(tau1/tau3)
denominador1=6*r2min**3+mu*(tau*tau-tau3*tau3)
srho1=(1.0/D0)*(((term5+term6)/denominador1)-D[0][0])

srho2=A+mu*B/r2min**3

term7=6*(D[0][2]*(tau3/tau1)-D[1][2]*(tau/tau1))*r2min**3
term8=mu*D[0][2]*(tau*tau-tau3*tau3)*(tau3/tau1)
denominador2=6*r2min**3+mu*(tau*tau-tau1*tau1)
srho3=(1.0/D0)*(((term7+term8)/denominador2)-D[2][2])

print'SLANT RANGES'
print 'rho_s1= '+str(srho1)+' km'
print 'rho_s2= '+str(srho2)+' km'
print 'rho_s3= '+str(srho3)+' km'

print '################################################'
print 'POSICIONES'
# STEP 10 Posiciones Vectoriales
r1_vect=[]
r2_vect=[]
r3_vect=[]
rho1=np.array(rho1)
rho2=np.array(rho2)
rho3=np.array(rho3)

r1_vect=[srho1*rho1[0],srho1*rho1[1],srho1*rho1[2]]+R1
r2_vect=[srho2*rho2[0],srho2*rho2[1],srho2*rho2[2]]+R1
r3_vect=[srho3*rho3[0],srho3*rho3[1],srho3*rho3[2]]+R1

print 'r1 ='+str(r1_vect)+' km'
print 'r2 ='+str(r2_vect)+' km'
print 'r3 ='+str(r3_vect)+' km'

print '################################################'
#  STEP 11 - Lagrange Coeficientes f1,g1,f3,g3

f1=1-(1./2)*(mu/r2min**3)*tau1*tau1
g1=tau1-(1./6)*(mu/r2min**3)*tau1**3

f3=1-(1./2)*(mu/r2min**3)*tau3*tau3
g3=tau3-(1./6)*(mu/r2min**3)*tau3**3

# STEP 12 - CALCULO DE V2
print 'VELOCIDAD'
v2=[]
v2=(1./(f1*g3-f3*g1))*(-f3*r1_vect+f1*r3_vect)
print 'v2= '+str(v2)+' km/seg'

