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

w0= np.power((e2**-1), 1/6) #modulo de los polos (radio de la circunferencia)

#%% Defino la transferencia

# TF hallada despejando coeficientes a, b y c
my_tf_coef = TransferFunction( [e**(-1)], [1, 2*e**(-1/3), 2*e**(-2/3), e**(-1)] )

# TF hallada a partir del mapa de polos y ceros
my_tf_pz = TransferFunction( [w0**3], [1, 2*w0, 2*w0**2, w0**3] )
#%% Gráficos
plt.close('all')

# TF_COEF
bodePlot(my_tf_coef, fig_id=1, filter_description = 'Coeficientes')
pzmap(my_tf_coef, fig_id=2, filter_description = 'Coeficientes') #S plane pole/zero plot
GroupDelay(my_tf_coef, fig_id=3, filter_description = 'Coeficientes')

# TF_PZ
bodePlot(my_tf_pz, fig_id=1, filter_description = 'Polos')
pzmap(my_tf_pz, fig_id=2, filter_description = 'Polos') #S plane pole/zero plot
GroupDelay(my_tf_pz, fig_id=3, filter_description = 'Polos')