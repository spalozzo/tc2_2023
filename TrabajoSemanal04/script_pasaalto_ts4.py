# -*- coding: utf-8 -*-
"""
Created on Tue May 23 16:49:03 2023

Trabajo Semanal 4: diseño de un filtro pasaalto MP a partir de una
plantilla usando el prototipo del pasabajo y la transformacion en frecuencia

@author: Santiago Palozzo
"""

#%% Inicializacion de librerias
# Librerías externas NumPy, SciPy y Matplotlib
from scipy.signal import TransferFunction
import matplotlib.pyplot as plt
import numpy as np

# Librería de TC2
import pytc2.sistemas_lineales as tc2

#%% Defino los parametros del filtro
fp= 40 * 10**3 #40 kHz
fs= 10 * 10**3 #10 kHz

wp= 2*np.pi*fp
ws= 2*np.pi*fs

norma_w= wp

wp_n= wp/norma_w # 1 rad/s
ws_n= ws/norma_w # 0.25 rad/s

alfa_min= 30 #dB
alfa_max= 1  #dB

# Realizo la transformacion en frecuencia hacia el prototipo pasabajo

Wp_n= 1/wp_n
Ws_n= 1/ws_n

ee2= 10**(alfa_max/10)-1 #epsilon**2
ee = np.sqrt(ee2)


# Consigo el orden del filtro "n" iterando
n=1
alfa_prueba= 10*np.log10(1+(ee2*np.power(Ws_n, 2*n)))
while alfa_prueba<alfa_min:
    n= n+1
    alfa_prueba= 10*np.log10(1+(ee2*np.power(Ws_n, 2*n)))
    
w_butter= np.power(ee, -1/n)

w0= wp_n * w_butter ## desnormalizo por w_butter
qq= 1
#%% Simulacion del filtro

### Prototipo Pasabajo
num1_lp,den1_lp= [w0],[1, w0] #Primer orden
num2_lp,den2_lp= [w0**2],[1, w0/qq, w0**2] #Segundo orden

my_lp= TransferFunction(np.polymul(num1_lp, num2_lp),np.polymul(den1_lp, den2_lp))

plt.close('all')
#tc2.analyze_sys(my_lp, sys_name="Prototipo Pasabajo")

### Transformacion a Pasaaltoo
num1_hp,den1_hp= [1, 0],[1, 1/w0] #Primer orden
num2_hp,den2_hp= [1, 0, 0],[1, 1/w0/qq, 1/w0**2] #Segundo orden
my_hp= TransferFunction(np.polymul(num1_hp, num2_hp),np.polymul(den1_hp, den2_hp))

#El denominador se mantuvo igual

tc2.analyze_sys(my_hp, sys_name="Pasaalto Transformado")




















