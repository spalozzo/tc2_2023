# -*- coding: utf-8 -*-
"""
Created on Mon May  1 14:37:03 2023

Trabajo Semanal 3: Diseño de un filtro pasabajos con el criterio de maxima
planicidad a partir de una plantilla.

@author: Santiago Palozzo
"""

#%% Inicializacion de librerias
# Librerías externas NumPy, SciPy y Matplotlib
from scipy.signal import TransferFunction
import matplotlib.pyplot as plt
import numpy as np

# Librería de TC2
from pytc2.sistemas_lineales import pzmap, GroupDelay, bodePlot

#%% Defino los parametros
alfa_max= 1     #[dB]
alfa_min= 12    #[dB]
wp= 1500    #[Hz]
ws= 3000    #[Hz]
wn= wp      #Norma de frecuencia
e2= 10**(alfa_max/10)-1 #epsilon**2
e = np.sqrt(e2);        #epsilon 
n = 3 #grado del filtro

cond_capacitores= False

#%% Defino los componentes del circuito
w0= np.power((e2**-1), 1/6) #modulo de los polos (radio de la circunferencia)
#w0= 1

qq= 1
norma_r= 1; norma_w= w0;

r1= norma_r
c1= 1/(norma_r * norma_w)
r2= norma_r
l2= (qq * norma_r)/norma_w
c2= 1/(qq * norma_r * norma_w)

#%% Redefino la norma de impedancia en el caso de usar C=100nF
norma_c= 10*10**(-6); #100nF

### CONDICION PARA EJECUTAR ESTE CIRCUITO
### Si esta comentado, retoma la norma_r
cond_capacitores= True

if cond_capacitores==True:
    r1= 1/(norma_c * norma_w)
    c1= norma_c
    r2= 1/(qq * norma_c * norma_w)
    l2= 1/(w0**2 * norma_c)
    c2= norma_c


#%% Defino las transferencias

# TF hallada despejando coeficientes a, b y c
my_tf_coef = TransferFunction( [e**(-1)], [1, 2*e**(-1/3), 2*e**(-2/3), e**(-1)] )

# TF hallada a partir del mapa de polos y ceros
my_tf_pz = TransferFunction( [w0**3], [1, 2*w0, 2*w0**2, w0**3] )

# TF hallada a partir del circuito implementado
tf_circ_num1er= [1/(r1*c1)]
tf_circ_den1er= [1, 1/(r1*c1)]

tf_circ_num2do= [1/(l2*c2)]
tf_circ_den2do= [1, r2/l2, 1/(l2*c2)]

my_tf_circ = TransferFunction( np.polymul(tf_circ_num1er, tf_circ_num2do), 
                              np.polymul(tf_circ_den1er, tf_circ_den2do))
#%% Gráficos
plt.close('all')

my_tf_array= [my_tf_coef, my_tf_pz, my_tf_circ]
my_tf_descriptions= ["Coeficientes", "Polos", "Circuito"]

for tf_2plot in range(len(my_tf_array)):
    bodePlot(my_tf_array[tf_2plot], fig_id=1, filter_description = my_tf_descriptions[tf_2plot])
    pzmap(my_tf_array[tf_2plot], fig_id=2, filter_description = my_tf_descriptions[tf_2plot]) #S plane pole/zero plot
    GroupDelay(my_tf_array[tf_2plot], fig_id=3, filter_description = my_tf_descriptions[tf_2plot])

### Si los calculos son correctos, todos los graficos se solapan.

# TF_COEF
#bodePlot(my_tf_coef, fig_id=1, filter_description = 'Coeficientes')
#pzmap(my_tf_coef, fig_id=2, filter_description = 'Coeficientes') #S plane pole/zero plot
#GroupDelay(my_tf_coef, fig_id=3, filter_description = 'Coeficientes')

# TF_PZ
#bodePlot(my_tf_pz, fig_id=1, filter_description = 'Polos')
#pzmap(my_tf_pz, fig_id=2, filter_description = 'Polos') #S plane pole/zero plot
#GroupDelay(my_tf_pz, fig_id=3, filter_description = 'Polos')